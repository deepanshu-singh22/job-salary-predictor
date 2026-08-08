"""
Loads and cleans the jobs dataset, handling malformed/quoted CSV lines,
and exposes helper functions for skills analysis.
"""

import time
import csv
import re
import pandas as pd
import numpy as np
from collections import Counter

import config
from config import ROLE_SKILLS_DATA_PATH

_cache = {"df": None, "loaded_at": 0}


def clean_skill_string(text: str) -> str:
    """Removes HTML tags and cleans extra whitespace from skill text."""
    if not isinstance(text, str):
        return ""
    cleaned = re.sub(r'<[^>]+>', ' ', text)
    return re.sub(r'\s+', ' ', cleaned).strip()


def _load_and_clean() -> pd.DataFrame:
    rows = []
    
    with open(config.DATA_PATH, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip().rstrip(",")
            if line.startswith('"') and line.endswith('"'):
                line = line[1:-1]
            line = line.replace('""', '"')
            
            try:
                parsed_row = list(csv.reader([line]))[0]
                rows.append(parsed_row)
            except Exception:
                continue

    if not rows:
        return pd.DataFrame()

    header = [col.strip() for col in rows[0]]
    data = [r for r in rows[1:] if len(r) == len(header)]
    
    df = pd.DataFrame(data, columns=header)

    df = df.rename(columns=config.COLUMNS)
    if "tagsAndSkills" in df.columns and "skills" not in df.columns:
        df = df.rename(columns={"tagsAndSkills": "skills"})

    if "skills" in df.columns:
        df = df[df["skills"].notna()]
        df["skills"] = df["skills"].astype(str).str.strip()
        df = df[(df["skills"] != "") & (df["skills"].str.lower() != "nan")]

    return df.reset_index(drop=True)


def get_df(force_reload: bool = False) -> pd.DataFrame:
    """In-memory cached DataFrame."""
    now = time.time()
    if (
        force_reload
        or _cache["df"] is None
        or (config.CACHE_TTL_SECONDS > 0 and now - _cache["loaded_at"] > config.CACHE_TTL_SECONDS)
    ):
        _cache["df"] = _load_and_clean()
        _cache["loaded_at"] = now
    return _cache["df"]


def get_skill_counts() -> pd.DataFrame:
    """Returns top overall skills (cleaned from HTML and long sentences)."""
    df = get_df()

    if "skills" not in df.columns or df["skills"].empty:
        return pd.DataFrame(columns=["skill_name", "frequency_count", "percentage_of_jobs", "rank"])

    exploded = (
        df["skills"]
        .dropna()
        .astype(str)
        .apply(clean_skill_string)
        .str.split(r"[,;|\n\r\t]")
        .explode()
        .str.strip()
    )
    
    exploded = exploded[
        (exploded != "") 
        & (exploded.str.lower() != "nan")
        & (exploded.str.len() <= 35)
        & (exploded.str.len() >= 2)
    ]

    if exploded.empty:
        return pd.DataFrame(columns=["skill_name", "frequency_count", "percentage_of_jobs", "rank"])

    temp = pd.DataFrame({"raw_skill": exploded, "skill_key": exploded.str.lower()})
    display_names = temp.groupby("skill_key")["raw_skill"].agg(
        lambda x: x.value_counts().idxmax()
    )

    total_jobs = len(df)
    counts = temp["skill_key"].value_counts().reset_index()
    counts.columns = ["skill_key", "frequency_count"]

    counts["skill_name"] = counts["skill_key"].map(display_names)
    counts["percentage_of_jobs"] = (counts["frequency_count"] / total_jobs * 100).round(2)
    counts["rank"] = range(1, len(counts) + 1)

    return counts[["skill_name", "frequency_count", "percentage_of_jobs", "rank"]]


def get_unique_job_roles() -> list:
    """Returns a sorted list of unique job titles for dropdowns."""
    df = get_df()
    if "job_title_normalized" not in df.columns:
        return []

    roles = df["job_title_normalized"].dropna().astype(str).str.strip()
    roles = roles[(roles != "") & (roles.str.lower() != "nan")].unique().tolist()
    return sorted(roles)


def get_skills_by_job_role(job_role: str, top_n: int = 10) -> pd.DataFrame:
    """Calculates skill frequency and demand percentage for a specific job role."""
    df = get_df()

    if "job_title_normalized" not in df.columns or "skills" not in df.columns or df.empty:
        return pd.DataFrame(columns=[
            "rank", "skill_name", "count_in_role", "percentage_demand_in_role", "job_role_selected"
        ])

    role_df = df[df["job_title_normalized"].astype(str).str.strip().str.lower() == job_role.strip().lower()]
    total_role_jobs = len(role_df)

    if total_role_jobs == 0:
        return pd.DataFrame(columns=[
            "rank", "skill_name", "count_in_role", "percentage_demand_in_role", "job_role_selected"
        ])

    exploded = (
        role_df["skills"]
        .dropna()
        .astype(str)
        .apply(clean_skill_string)
        .str.split(r"[,;|\n\r\t]")
        .explode()
        .str.strip()
    )
    
    exploded = exploded[
        (exploded != "") 
        & (exploded.str.lower() != "nan")
        & (exploded.str.len() <= 35)
        & (exploded.str.len() >= 2)
    ]

    if exploded.empty:
        return pd.DataFrame(columns=[
            "rank", "skill_name", "count_in_role", "percentage_demand_in_role", "job_role_selected"
        ])

    temp = pd.DataFrame({"raw_skill": exploded, "skill_key": exploded.str.lower()})
    display_names = temp.groupby("skill_key")["raw_skill"].agg(
        lambda x: x.value_counts().idxmax()
    )

    counts = temp["skill_key"].value_counts().head(top_n).reset_index()
    counts.columns = ["skill_key", "count_in_role"]

    counts["rank"] = range(1, len(counts) + 1)
    counts["skill_name"] = counts["skill_key"].map(display_names)
    counts["percentage_demand_in_role"] = ((counts["count_in_role"] / total_role_jobs) * 100).round(1)
    counts["job_role_selected"] = job_role

    return counts[["rank", "skill_name", "count_in_role", "percentage_demand_in_role", "job_role_selected"]]


def get_top_hiring_locations(top_n=20) -> pd.DataFrame:
    """Calculates top hiring locations with salary metrics & dominant skills."""
    try:
        df = pd.read_csv(ROLE_SKILLS_DATA_PATH, low_memory=False)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return pd.DataFrame()

    for col in ['salary_avg', 'minimumSalary', 'maximumSalary']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    def extract_primary_city(loc_str):
        if not isinstance(loc_str, str) or not loc_str.strip():
            return "Unknown"
        first_part = loc_str.split(',')[0].split('(')[0].strip()
        first_part = re.sub(r'^(Hybrid|Remote)\s*-\s*', '', first_part, flags=re.IGNORECASE).strip()
        return first_part if first_part else "Unknown"

    if 'location' not in df.columns:
        return pd.DataFrame()

    df['city'] = df['location'].apply(extract_primary_city)
    df_filtered = df[~df['city'].isin(["Remote", "Unknown", "Other", ""])]

    def get_top_skills(skills_series, top_k=3):
        skills_list = []
        for skill_str in skills_series.dropna():
            cleaned = re.sub(r'<[^>]+>', ' ', str(skill_str))
            tokens = [s.strip() for s in re.split(r'[,;|\n\r\t]', cleaned) if s.strip()]
            skills_list.extend(tokens)
        counts = Counter(skills_list)
        return ", ".join([skill for skill, _ in counts.most_common(top_k)])

    location_stats = []
    grouped = df_filtered.groupby('city')

    for city, group in grouped:
        job_count = len(group)
        valid_salaries = group[group['salary_avg'] > 0]['salary_avg'] if 'salary_avg' in group.columns else pd.Series()
        avg_salary = valid_salaries.mean() if not valid_salaries.empty else 0
        median_salary = valid_salaries.median() if not valid_salaries.empty else 0
        
        min_sal = group[group['minimumSalary'] > 0]['minimumSalary'].min() if 'minimumSalary' in group.columns else 0
        min_sal = min_sal if not (pd.isna(min_sal) or np.isnan(min_sal)) else 0
        
        max_sal = group[group['maximumSalary'] > 0]['maximumSalary'].max() if 'maximumSalary' in group.columns else 0
        max_sal = max_sal if not (pd.isna(max_sal) or np.isnan(max_sal)) else 0
        
        skills_col = 'tagsAndSkills' if 'tagsAndSkills' in group.columns else 'skills'
        dominant_skills = get_top_skills(group[skills_col]) if skills_col in group.columns else ""
        
        location_stats.append({
            'city': city,
            'job_count': job_count,
            'avg_salary_lpa': round(avg_salary / 100000, 2),
            'median_salary_lpa': round(median_salary / 100000, 2),
            'salary_min_lpa': round(min_sal / 100000, 2),
            'salary_max_lpa': round(max_sal / 100000, 2),
            'dominant_skills': dominant_skills
        })

    if not location_stats:
        return pd.DataFrame()

    top_df = pd.DataFrame(location_stats).sort_values(by='job_count', ascending=False)
    return top_df.head(top_n).reset_index(drop=True)


def get_top_high_paying_roles(top_n: int = 10, min_job_count: int = 1) -> pd.DataFrame:
    """Calculates top high paying job roles with accurate min/max salary ranges."""
    df = get_df()
    
    if df is None or df.empty:
        return pd.DataFrame()

    role_col = 'job_title_normalized' if 'job_title_normalized' in df.columns else 'title'
    salary_col = 'salary_avg' if 'salary_avg' in df.columns else None

    if role_col not in df.columns or salary_col not in df.columns:
        return pd.DataFrame()

    df_clean = df.copy()

    # Convert numeric
    df_clean['salary_avg'] = pd.to_numeric(df_clean[salary_col], errors='coerce').fillna(0)
    
    # Check column aliases for minimum & maximum salary
    min_col = 'minimumSalary' if 'minimumSalary' in df_clean.columns else ('salary_min' if 'salary_min' in df_clean.columns else None)
    max_col = 'maximumSalary' if 'maximumSalary' in df_clean.columns else ('salary_max' if 'salary_max' in df_clean.columns else None)

    df_clean['sal_min'] = pd.to_numeric(df_clean[min_col], errors='coerce').fillna(0) if min_col else 0.0
    df_clean['sal_max'] = pd.to_numeric(df_clean[max_col], errors='coerce').fillna(0) if max_col else 0.0

    # Filter rows with salary > 0
    df_clean = df_clean[df_clean['salary_avg'] > 0]

    if df_clean.empty:
        return pd.DataFrame()

    job_col = 'jobId' if 'jobId' in df_clean.columns else df_clean.columns[0]
    grouped = df_clean.groupby(role_col)
    
    roles_df = grouped.agg(
        job_count=(job_col, 'count'),
        salary_avg=('salary_avg', 'mean'),
        salary_median=('salary_avg', 'median'),
        salary_min=('sal_min', 'min'),
        salary_max=('sal_max', 'max')
    ).reset_index()

    roles_df = roles_df.rename(columns={role_col: 'job_title_normalized'})
    roles_df = roles_df[roles_df['job_count'] >= min_job_count]

    roles_df = roles_df.sort_values(by='salary_avg', ascending=False).head(top_n).reset_index(drop=True)
    roles_df['rank'] = roles_df.index + 1

    roles_df['salary_avg'] = roles_df['salary_avg'].round(2)
    roles_df['salary_median'] = roles_df['salary_median'].round(2)

    # Convert Lakhs format for salary range (e.g. ₹0.0 - ₹70.0L)
    roles_df['salary_range'] = roles_df.apply(
        lambda r: f"₹{r['salary_min']/100000:.1f} - ₹{r['salary_max']/100000:.1f}L" if r['salary_max'] >= 100000 else f"₹{r['salary_min']:,.0f} - ₹{r['salary_max']:,.0f}", axis=1
    )

    return roles_df






# ==========================================
# SKILL NETWORK GRAPH GENERATOR
# ==========================================
from itertools import combinations
import networkx as nx
from pyvis.network import Network

def get_skill_network_html(top_n_skills: int = 22) -> str:
    """Generates a PyVis 360-degree rotating network graph with a modern dark GUI card."""
    df = get_df()
    
    # Identify skills column
    skills_col = "skills" if "skills" in df.columns else ("tagsAndSkills" if "tagsAndSkills" in df.columns else None)
    if not skills_col or df.empty:
        return "<div style='color:white;'>No skill data available for network graph.</div>"

    job_skills_list = []
    skill_freq = Counter()
    
    # Process skills safely
    for skills_str in df[skills_col].dropna():
        cleaned = clean_skill_string(str(skills_str))
        skills = list(set([s.strip().title() for s in re.split(r'[,;|\n\r\t]', cleaned) if len(s.strip()) >= 2 and len(s.strip()) <= 35]))
        for s in skills:
            skill_freq[s] += 1
        job_skills_list.append(skills)

    top_skills = [s for s, c in skill_freq.most_common(top_n_skills)]
    top_skills_set = set(top_skills)

    # Co-occurrence calculation
    pair_counts = Counter()
    for skills in job_skills_list:
        filtered = [s for s in skills if s in top_skills_set]
        if len(filtered) > 1:
            pair_counts.update(combinations(sorted(filtered), 2))

    # NetworkX Graph
    G = nx.Graph()
    for skill in top_skills:
        G.add_node(skill, frequency=skill_freq[skill])
        
    for (s1, s2), count in pair_counts.items():
        if count >= 2:
            G.add_edge(s1, s2, weight=count)

    if len(G.nodes) == 0:
        return "<div style='color:white;'>Not enough co-occurrence data to build network graph.</div>"

    max_f = max([G.nodes[n]['frequency'] for n in G.nodes()])
    
    # Assign Tiers
    tier_map = {}
    tier_groups = {1: [], 2: [], 3: []}
    for node in G.nodes():
        freq = G.nodes[node]['frequency']
        if freq >= max_f * 0.40:
            level = 1
        elif freq >= max_f * 0.18:
            level = 2
        else:
            level = 3
        tier_map[node] = level
        tier_groups[level].append(node)

    # PyVis Network Init
    net = Network(height="620px", width="100%", bgcolor="#0F172A", font_color="#FFFFFF", cdn_resources='in_line')
    
    # Add Nodes
    for node in G.nodes():
        node_level = tier_map[node]
        freq = G.nodes[node]['frequency']
        node_size = int(max(20, (freq / max_f) * 55))
        
        same_lvl_skills = [s for s in tier_groups[node_level] if s != node]
        conn_skills = list(G.neighbors(node))
        
        base_color = "#F97316" if node_level == 1 else ("#FBBF24" if node_level == 2 else "#38BDF8")
        
        net.add_node(
            node, 
            label=node, 
            title="",  # Disables default browser tooltip
            size=node_size,
            color={
                'background': base_color,
                'border': '#FFFFFF',
                'highlight': {'background': '#00FFCC', 'border': '#FFFFFF'},
                'hover': {'background': '#FF007F', 'border': '#FFFFFF'}
            },
            font={'size': 14, 'color': '#FFFFFF', 'face': 'Arial Black'},
            level=f"Tier {node_level}",
            freq=f"{freq:,}",
            same_skills=", ".join(same_lvl_skills[:5]) if same_lvl_skills else "None",
            conn_skills=", ".join(conn_skills[:5]) if conn_skills else "None"
        )

    # Add Edges
    for s1, s2, data in G.edges(data=True):
        net.add_edge(s1, s2, value=data['weight'], color={'color': 'rgba(148, 163, 184, 0.25)', 'highlight': '#00FFCC'})

    # Custom Options
    net.set_options("""
    var options = {
      "nodes": {
        "shadow": {
          "enabled": true,
          "color": "rgba(0,255,204,0.8)",
          "size": 18,
          "x": 0, "y": 0
        }
      },
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -50,
          "centralGravity": 0.01,
          "springLength": 100,
          "springConstant": 0.08
        },
        "solver": "forceAtlas2Based"
      },
      "interaction": {
        "hover": true,
        "navigationButtons": true,
        "multiselect": true
      }
    }
    """)

    html_content = net.generate_html()

    # MODERN GLASSMORPHISM GUI + CONTINUOUS 360 ROTATION INJECTION
    custom_gui_and_rotation = """
    <div id="modern-gui-card" style="
        position: absolute;
        top: 15px;
        right: 15px;
        width: 270px;
        background: rgba(15, 23, 42, 0.88);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(56, 189, 248, 0.4);
        box-shadow: 0 8px 32px 0 rgba(0, 255, 204, 0.2);
        border-radius: 12px;
        padding: 15px;
        color: #FFFFFF;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        z-index: 999;
        pointer-events: none;
    ">
        <div style="font-size: 10px; text-transform: uppercase; color: #38BDF8; font-weight: bold; margin-bottom: 2px;">Skill Network Insights</div>
        <div id="gui-title" style="font-size: 18px; font-weight: 800; color: #00FFCC; margin-bottom: 8px;">Hover or Click Node</div>
        
        <div style="display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 12px;">
            <span style="color: #94A3B8;">Demand Tier:</span>
            <span id="gui-level" style="font-weight: 600; color: #FBBF24;">--</span>
        </div>
        
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 12px;">
            <span style="color: #94A3B8;">Jobs Count:</span>
            <span id="gui-freq" style="font-weight: 600; color: #38BDF8;">--</span>
        </div>
        
        <hr style="border: none; border-top: 1px solid rgba(255,255,255,0.1); margin: 6px 0;">
        
        <div style="margin-bottom: 6px;">
            <div style="font-size: 11px; color: #FBBF24; font-weight: 600; margin-bottom: 2px;">⚡ Same-Demand Skills:</div>
            <div id="gui-same" style="font-size: 11px; color: #CBD5E1; line-height: 1.3;">Hover over a skill node...</div>
        </div>
        
        <div>
            <div style="font-size: 11px; color: #00FFCC; font-weight: 600; margin-bottom: 2px;">🔗 Connected Skills:</div>
            <div id="gui-conn" style="font-size: 11px; color: #CBD5E1; line-height: 1.3;">Hover over a skill node...</div>
        </div>
    </div>

    <script type="text/javascript">
        window.addEventListener("load", function() {
            setTimeout(function() {
                var speed = 0.003;
                
                if (typeof network !== 'undefined') {
                    network.on("hoverNode", function (params) {
                        var nodeId = params.node;
                        var nodeData = network.body.nodes[nodeId].options;
                        
                        document.getElementById('gui-title').innerText = nodeId;
                        document.getElementById('gui-level').innerText = nodeData.level;
                        document.getElementById('gui-freq').innerText = nodeData.freq;
                        document.getElementById('gui-same').innerText = nodeData.same_skills;
                        document.getElementById('gui-conn').innerText = nodeData.conn_skills;
                    });
                    
                    network.on("selectNode", function (params) {
                        var nodeId = params.nodes[0];
                        var nodeData = network.body.nodes[nodeId].options;
                        
                        document.getElementById('gui-title').innerText = nodeId;
                        document.getElementById('gui-level').innerText = nodeData.level;
                        document.getElementById('gui-freq').innerText = nodeData.freq;
                        document.getElementById('gui-same').innerText = nodeData.same_skills;
                        document.getElementById('gui-conn').innerText = nodeData.conn_skills;
                    });
                }
                
                function autoRotate() {
                    if (typeof network !== 'undefined') {
                        var pos = network.getPositions();
                        var keys = Object.keys(pos);
                        if (keys.length > 0) {
                            var cosA = Math.cos(speed);
                            var sinA = Math.sin(speed);
                            
                            keys.forEach(function(id) {
                                var x = pos[id].x;
                                var y = pos[id].y;
                                var nx = x * cosA - y * sinA;
                                var ny = x * sinA + y * cosA;
                                network.body.nodes[id].x = nx;
                                network.body.nodes[id].y = ny;
                            });
                            network.redraw();
                        }
                    }
                    requestAnimationFrame(autoRotate);
                }
                autoRotate();
            }, 800);
        });
    </script>
    </body>
    """
    
    
    return html_content.replace("</body>", custom_gui_and_rotation)
