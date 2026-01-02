# app.py
from flask import Flask, request
import random

from backend import (
    load_asep_project_titles,
    load_psp_cp_titles,
    load_wd_cp_titles,
    load_da_cp_titles,
    load_pfe_cp_titles,
    load_aem_cp_titles,
)

app = Flask(__name__)


def get_random_ideas(titles, count=5):
    """Backend helper: returns a list of random ideas (no printing)."""
    if not titles:
        return []
    count = min(count, len(titles))
    return random.sample(titles, count)


@app.route("/", methods=["GET", "POST"])
def index():
    project_type = ""
    module = ""
    course = ""
    ideas = []

    if request.method == "POST":
        project_type = request.form.get("project_type", "")
        module = request.form.get("module", "")
        course = request.form.get("course", "")

        # ASEP directly
        if project_type == "asep":
            titles = load_asep_project_titles()
            ideas = get_random_ideas(titles)

        # Course project
        elif project_type == "course":
            titles = []

            if module == "m1":
                if course == "psp":
                    titles = load_psp_cp_titles()
                elif course == "wd":
                    titles = load_wd_cp_titles()
            elif module == "m2":
                if course == "da":
                    titles = load_da_cp_titles()
                elif course == "pfe":
                    titles = load_pfe_cp_titles()
                elif course == "aem":
                    titles = load_aem_cp_titles()

            ideas = get_random_ideas(titles)

    # ---------- HTML (frontend) ----------

    # Step 1 dropdown
    step1_html = f"""
    <form method="POST" class="step-form">
        <table class="form-table">
            <tr>
                <th><span class="step-badge">1</span> Project Type</th>
                <td>
                    <label for="project_type" class="field-label">Select Project Type</label><br>
                    <select name="project_type" id="project_type" required class="select-input">
                        <option value="">-- Select --</option>
                        <option value="asep" {"selected" if project_type=="asep" else ""}>ASEP Project</option>
                        <option value="course" {"selected" if project_type=="course" else ""}>Course Project</option>
                    </select>
                </td>
                <td class="btn-cell">
                    <button type="submit" class="btn primary">Next</button>
                </td>
            </tr>
        </table>
    </form>
    """

    # Step 2 (module) – only if Course selected
    if project_type == "course":
        step2_html = f"""
        <form method="POST" class="step-form">
            <input type="hidden" name="project_type" value="course">
            <table class="form-table">
                <tr>
                    <th><span class="step-badge">2</span> Module</th>
                    <td>
                        <label for="module" class="field-label">Select Module</label><br>
                        <select name="module" id="module" required class="select-input">
                            <option value="">-- Select Module --</option>
                            <option value="m1" {"selected" if module=="m1" else ""}>Module 1</option>
                            <option value="m2" {"selected" if module=="m2" else ""}>Module 2</option>
                        </select>
                    </td>
                    <td class="btn-cell">
                        <button type="submit" class="btn primary">Next</button>
                    </td>
                </tr>
            </table>
        </form>
        """
    else:
        step2_html = ""

    # Step 3 (course) – only if module chosen
    if project_type == "course" and module:
        if module == "m1":
            course_options_html = f"""
                <option value="">-- Select Course --</option>
                <option value="psp" {"selected" if course=="psp" else ""}>Problem Solving & Programming (PSP)</option>
                <option value="wd" {"selected" if course=="wd" else ""}>Web Development</option>
            """
        else:
            course_options_html = f"""
                <option value="">-- Select Course --</option>
                <option value="da" {"selected" if course=="da" else ""}>Data Analysis (DA)</option>
                <option value="pfe" {"selected" if course=="pfe" else ""}>Python for Engineers (PFE)</option>
                <option value="aem" {"selected" if course=="aem" else ""}>Applied Electromechanics (AEM)</option>
            """

        step3_html = f"""
        <form method="POST" class="step-form">
            <input type="hidden" name="project_type" value="course">
            <input type="hidden" name="module" value="{module}">
            <table class="form-table">
                <tr>
                    <th><span class="step-badge">3</span> Course</th>
                    <td>
                        <label for="course" class="field-label">Select Course</label><br>
                        <select name="course" id="course" required class="select-input">
                            {course_options_html}
                        </select>
                    </td>
                    <td class="btn-cell">
                        <button type="submit" class="btn success">Generate Ideas</button>
                    </td>
                </tr>
            </table>
        </form>
        """
    else:
        step3_html = ""

    # Ideas table
    ideas_rows = "".join(
        f"<tr class='ideas-row'><td>{i+1}</td><td>{idea}</td></tr>"
        for i, idea in enumerate(ideas)
    )
    ideas_table_html = f"""
    <table class="ideas-table">
        <tr>
            <th>#</th>
            <th>Project Idea</th>
        </tr>
        {ideas_rows if ideas_rows else '<tr><td colspan="2" class="no-ideas">No ideas generated yet. Make a selection above.</td></tr>'}
    </table>
    """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Project Idea Generator</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                background: linear-gradient(135deg, #1e3c72, #2a5298, #4b79a1);
                background-size: 200% 200%;
                animation: bgGradient 12s ease infinite;
            }}
            @keyframes bgGradient {{
                0% {{ background-position: 0% 50%; }}
                50% {{ background-position: 100% 50%; }}
                100% {{ background-position: 0% 50%; }}
            }}
            .container {{
                width: 95%;
                max-width: 950px;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border-radius: 18px;
                padding: 28px 32px 32px;
                box-shadow: 0 18px 40px rgba(0,0,0,0.35);
                color: #ffffff;
                animation: fadeInUp 0.7s ease-out;
                border: 1px solid rgba(255,255,255,0.25);
            }}
            @keyframes fadeInUp {{
                0% {{ opacity: 0; transform: translateY(25px) scale(0.98); }}
                100% {{ opacity: 1; transform: translateY(0) scale(1); }}
            }}
            .title {{
                text-align: center;
                margin: 0 0 10px 0;
                font-size: 30px;
                letter-spacing: 2px;
                text-transform: uppercase;
                background: linear-gradient(90deg, #ffcc33, #ff6699, #66ffff);
                -webkit-background-clip: text;
                background-clip: text;
                color: transparent;
                animation: glow 2.8s ease-in-out infinite;
            }}
            @keyframes glow {{
                0% {{ text-shadow: 0 0 5px rgba(255,255,255,0.3); }}
                50% {{ text-shadow: 0 0 16px rgba(255,255,255,0.9); }}
                100% {{ text-shadow: 0 0 5px rgba(255,255,255,0.3); }}
            }}
            .subtitle {{
                text-align: center;
                margin: 0 0 25px 0;
                color: #dfe8ff;
                font-size: 14px;
                opacity: 0.9;
            }}
            h3.section-title {{
                margin-top: 20px;
                margin-bottom: 8px;
                font-size: 18px;
                color: #eaf1ff;
            }}
            .step-form {{
                margin-bottom: 10px;
                animation: fadeIn 0.5s ease;
            }}
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(10px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            .form-table {{
                width: 100%;
                border-collapse: collapse;
                border-radius: 12px;
                overflow: hidden;
                background: rgba(255, 255, 255, 0.06);
                box-shadow: 0 8px 20px rgba(0,0,0,0.25);
            }}
            .form-table th, .form-table td {{
                padding: 12px 14px;
            }}
            .form-table th {{
                width: 24%;
                background: rgba(255, 255, 255, 0.08);
                font-weight: 600;
                font-size: 14px;
                border-right: 1px solid rgba(255,255,255,0.08);
            }}
            .form-table td {{
                font-size: 14px;
                vertical-align: middle;
            }}
            .field-label {{
                font-size: 13px;
                color: #d7e3ff;
            }}
            .select-input {{
                margin-top: 4px;
                width: 90%;
                max-width: 260px;
                padding: 6px 10px;
                border-radius: 8px;
                border: 1px solid rgba(255,255,255,0.4);
                background: rgba(6, 16, 40, 0.4);
                color: #ffffff;
                outline: none;
                font-size: 13px;
                backdrop-filter: blur(6px);
            }}
            .select-input:focus {{
                border-color: #ffcc66;
                box-shadow: 0 0 6px rgba(255, 204, 102, 0.7);
            }}
            .btn-cell {{
                text-align: right;
                white-space: nowrap;
            }}
            .btn {{
                border: none;
                border-radius: 999px;
                padding: 8px 18px;
                font-size: 13px;
                cursor: pointer;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                font-weight: 600;
                transition: transform 0.18s ease, box-shadow 0.18s ease, opacity 0.18s ease;
            }}
            .btn.primary {{
                background: linear-gradient(135deg, #4facfe, #00f2fe);
                color: #041322;
                box-shadow: 0 8px 18px rgba(0, 242, 254, 0.4);
            }}
            .btn.success {{
                background: linear-gradient(135deg, #43e97b, #38f9d7);
                color: #042011;
                box-shadow: 0 8px 18px rgba(72, 232, 140, 0.45);
            }}
            .btn:hover {{
                transform: translateY(-2px) scale(1.02);
                box-shadow: 0 10px 26px rgba(0,0,0,0.4);
                opacity: 0.95;
            }}
            .btn:active {{
                transform: translateY(0) scale(0.99);
                box-shadow: 0 4px 10px rgba(0,0,0,0.4);
                opacity: 0.9;
            }}
            .step-badge {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 22px;
                height: 22px;
                border-radius: 50%;
                background: radial-gradient(circle at 30% 30%, #ffffff, #ffcc33);
                color: #1b2338;
                font-size: 12px;
                margin-right: 8px;
                box-shadow: 0 0 6px rgba(255, 255, 255, 0.7);
            }}
            .ideas-wrapper {{
                margin-top: 24px;
            }}
            .ideas-table {{
                width: 100%;
                border-collapse: collapse;
                border-radius: 12px;
                overflow: hidden;
                background: rgba(2, 10, 30, 0.7);
                box-shadow: 0 10px 24px rgba(0,0,0,0.35);
            }}
            .ideas-table th, .ideas-table td {{
                padding: 10px 12px;
                border-bottom: 1px solid rgba(255,255,255,0.06);
                font-size: 14px;
            }}
            .ideas-table th {{
                background: rgba(255, 255, 255, 0.08);
                text-align: left;
            }}
            .ideas-table tr:last-child td {{
                border-bottom: none;
            }}
            .ideas-row {{
                animation: rowIn 0.35s ease-out;
            }}
            @keyframes rowIn {{
                from {{ opacity: 0; transform: translateX(-10px); }}
                to {{ opacity: 1; transform: translateX(0); }}
            }}
            .ideas-table tr:hover td {{
                background: rgba(255, 255, 255, 0.04);
            }}
            .no-ideas {{
                text-align: center;
                color: #c8d4ff;
                font-style: italic;
            }}
            .summary-table {{
                width: 100%;
                border-collapse: collapse;
                border-radius: 10px;
                overflow: hidden;
                margin-top: 14px;
                background: rgba(255, 255, 255, 0.06);
            }}
            .summary-table th, .summary-table td {{
                padding: 8px 10px;
                font-size: 13px;
                border-bottom: 1px solid rgba(255,255,255,0.08);
            }}
            .summary-table th {{
                width: 26%;
                background: rgba(255, 255, 255, 0.08);
                text-align: left;
            }}
            .summary-table tr:last-child th,
            .summary-table tr:last-child td {{
                border-bottom: none;
            }}
            .summary-label {{
                color: #dfe6ff;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="title">Project Idea Generator</h1>
            <p class="subtitle">Randomized ideas powered by your Python backend (CSV + random).</p>

            <h3 class="section-title">Selection Panel</h3>
            {step1_html}
            {step2_html}
            {step3_html}

            <div class="ideas-wrapper">
                <h3 class="section-title">Suggested Project Ideas</h3>
                {ideas_table_html}
            </div>

            <h3 class="section-title">Current Selection Summary</h3>
            <table class="summary-table">
                <tr>
                    <th class="summary-label">Project Type</th>
                    <td>{project_type or "Not selected"}</td>
                </tr>
                <tr>
                    <th class="summary-label">Module</th>
                    <td>{module or "Not selected / Not applicable"}</td>
                </tr>
                <tr>
                    <th class="summary-label">Course</th>
                    <td>{course or "Not selected / Not applicable"}</td>
                </tr>
            </table>
        </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)


    
