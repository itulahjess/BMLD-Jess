import streamlit as st


def apply_global_styles():
	st.markdown("""
	<style>
	/* ---------- GLOBAL PAGE STYLE ---------- */

	.stApp {
		background:
			radial-gradient(circle at top right, rgba(116, 222, 188, 0.22), transparent 34%),
			radial-gradient(circle at bottom left, rgba(203, 245, 229, 0.35), transparent 38%),
			#f5fbf8;
		color: #2f3038;
	}

	.block-container {
		padding-top: 2.2rem;
		padding-bottom: 3rem;
		max-width: 1100px;
	}

	/* ---------- TYPOGRAPHY ---------- */

	h1 {
		font-size: 52px !important;
		font-weight: 800 !important;
		letter-spacing: -1.8px !important;
		color: #2f3038 !important;
		margin-bottom: 1.2rem !important;
	}

	h2, h3 {
		color: #2f3038 !important;
		letter-spacing: -0.7px !important;
	}

	p, label, span {
		color: #2f3038;
	}

	/* ---------- PAGE INTRO ---------- */

	.page-intro {
		position: relative;
		overflow: hidden;
		background:
			linear-gradient(135deg, rgba(232, 255, 245, 0.96), rgba(255, 255, 255, 0.76));
		padding: 28px 32px;
		border-radius: 28px;
		border: 1px solid rgba(95, 208, 173, 0.18);
		box-shadow: 0 18px 45px rgba(31, 122, 99, 0.08);
		margin-bottom: 30px;
		backdrop-filter: blur(14px);
	}

	.page-intro::before {
		content: "";
		position: absolute;
		width: 190px;
		height: 190px;
		border-radius: 50%;
		background: rgba(95, 208, 173, 0.14);
		top: -80px;
		right: -60px;
	}

	.page-intro-title {
		position: relative;
		z-index: 1;
		font-size: 24px;
		font-weight: 900;
		color: #054033;
		margin-bottom: 6px;
	}

	.page-intro-text {
		position: relative;
		z-index: 1;
		font-size: 15px;
		color: #52796f;
		line-height: 1.5;
	}

	/* ---------- METRIC CARDS ---------- */

	div[data-testid="stMetric"] {
		background:
			linear-gradient(145deg, rgba(232, 255, 245, 0.95), rgba(255, 255, 255, 0.72));
		padding: 24px;
		border-radius: 24px;
		box-shadow: 0 14px 35px rgba(31, 122, 99, 0.08);
		border: 1px solid rgba(95, 208, 173, 0.17);
		backdrop-filter: blur(12px);
		min-height: 125px;
	}

	div[data-testid="stMetric"]:hover {
		transform: translateY(-4px);
		box-shadow: 0 20px 45px rgba(31, 122, 99, 0.14);
		border: 1px solid rgba(95, 208, 173, 0.32);
	}

	div[data-testid="stMetric"] label {
		font-size: 15px !important;
		font-weight: 800 !important;
		color: #054033 !important;
		line-height: 1.25 !important;
		white-space: normal !important;
	}

	div[data-testid="stMetric"] [data-testid="stMetricValue"] {
		font-size: 27px !important;
		font-weight: 900 !important;
		color: #1b5e54 !important;
		letter-spacing: -0.5px;
		white-space: normal !important;
	}

	div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
		display: none;
	}

	/* ---------- SECTION TITLES ---------- */

	.section-title {
		font-size: 32px;
		font-weight: 900;
		color: #2f3038;
		letter-spacing: -0.9px;
		margin-top: 10px;
		margin-bottom: 18px;
	}

	.section-subtitle {
		font-size: 15px;
		color: #6b9080;
		margin-top: -8px;
		margin-bottom: 18px;
	}

	/* ---------- EXPANDER ---------- */

	.streamlit-expanderHeader {
		background: rgba(255, 255, 255, 0.72);
		border-radius: 18px;
		border: 1px solid rgba(95, 208, 173, 0.18);
		font-weight: 800;
		color: #054033;
	}

	div[data-testid="stExpander"] {
		border: none;
		background: transparent;
	}

	div[data-testid="stExpander"] details {
		background: rgba(255, 255, 255, 0.5);
		border-radius: 22px;
		border: 1px solid rgba(95, 208, 173, 0.18);
		box-shadow: 0 14px 34px rgba(31, 122, 99, 0.06);
	}

	/* ---------- INPUTS ---------- */

	.stTextInput input,
	.stNumberInput input,
	.stDateInput input,
	.stSelectbox div[data-baseweb="select"],
	.stCheckbox {
		border-radius: 14px !important;
	}

	.stTextInput input,
	.stNumberInput input,
	.stDateInput input {
		background: rgba(255, 255, 255, 0.85) !important;
		border: 1px solid rgba(95, 208, 173, 0.22) !important;
		color: #2f3038 !important;
	}

	.stTextInput input:focus,
	.stNumberInput input:focus,
	.stDateInput input:focus {
		border-color: #5fd0ad !important;
		box-shadow: 0 0 0 3px rgba(95, 208, 173, 0.16) !important;
	}

	/* ---------- BUTTONS ---------- */

	.stButton > button {
		border-radius: 16px !important;
		border: 1px solid rgba(95, 208, 173, 0.26) !important;
		background: rgba(255, 255, 255, 0.78) !important;
		color: #054033 !important;
		font-weight: 800 !important;
		box-shadow: 0 8px 20px rgba(31, 122, 99, 0.08) !important;
		transition: all 0.2s ease !important;
	}

	.stButton > button:hover {
		transform: translateY(-2px);
		border: 1px solid rgba(95, 208, 173, 0.48) !important;
		box-shadow: 0 14px 28px rgba(31, 122, 99, 0.13) !important;
		background: #e8fff5 !important;
		color: #054033 !important;
	}

	/* ---------- TABS ---------- */

	button[data-baseweb="tab"] {
		font-size: 16px;
		font-weight: 700;
		color: #52796f;
		padding: 12px 18px;
		border-radius: 999px;
		margin-right: 8px;
		transition: all 0.2s ease;
	}

	button[data-baseweb="tab"]:hover {
		background: rgba(95, 208, 173, 0.12);
		color: #054033;
	}

	button[data-baseweb="tab"][aria-selected="true"] {
		background: #5fd0ad;
		color: white;
	}

	div[data-baseweb="tab-highlight"] {
		display: none;
	}

	/* ---------- BUDGET PAGE ---------- */

	.budget-category {
		font-size: 21px;
		font-weight: 900;
		color: #054033;
		margin-bottom: 8px;
	}

	.budget-label {
		font-size: 13px;
		font-weight: 800;
		color: #6b9080;
		margin-bottom: 4px;
	}

	.budget-value {
		font-size: 18px;
		font-weight: 900;
		color: #2f3038;
	}

	.budget-percent {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		padding: 8px 13px;
		border-radius: 999px;
		background: rgba(95, 208, 173, 0.16);
		color: #1f7a63;
		font-weight: 900;
		font-size: 14px;
	}

	.budget-separator {
		height: 1px;
		background: rgba(95, 208, 173, 0.14);
		margin: 22px 0;
	}

	/* ---------- SAVINGS GOALS PAGE ---------- */

	.goal-row-spacer {
		height: 18px;
	}

	.goal-title {
		font-size: 25px;
		font-weight: 900;
		color: #054033;
		letter-spacing: -0.4px;
		margin-bottom: 12px;
	}

	.goal-label {
		font-size: 13px;
		font-weight: 800;
		color: #6b9080;
		margin-bottom: 4px;
	}

	.goal-value {
		font-size: 17px;
		font-weight: 900;
		color: #2f3038;
		letter-spacing: -0.2px;
	}

	.goal-money {
		font-size: 15px;
		color: #52796f;
		margin-top: 10px;
	}

	.goal-percent {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		padding: 10px 16px;
		border-radius: 999px;
		background: rgba(95, 208, 173, 0.16);
		color: #1f7a63;
		font-weight: 900;
		font-size: 15px;
	}

	.goal-percent-warning {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		padding: 10px 16px;
		border-radius: 999px;
		background: rgba(255, 193, 7, 0.18);
		color: #8a6500;
		font-weight: 900;
		font-size: 15px;
	}

	.goal-percent-complete {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		padding: 10px 16px;
		border-radius: 999px;
		background: rgba(95, 208, 173, 0.25);
		color: #0b5f4d;
		font-weight: 900;
		font-size: 15px;
	}

	/* ---------- SUBSCRIPTION / ABO PAGES ---------- */

	.sub-icon {
		width: 54px;
		height: 54px;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 18px;
		background: linear-gradient(145deg, rgba(232, 255, 245, 1), rgba(255, 255, 255, 0.75));
		font-size: 28px;
		box-shadow:
			inset 0 0 0 1px rgba(95, 208, 173, 0.16),
			0 10px 22px rgba(31, 122, 99, 0.08);
	}

	.sub-name {
		font-size: 20px;
		font-weight: 900;
		color: #054033;
		margin-bottom: 4px;
		letter-spacing: -0.2px;
	}

	.sub-detail {
		font-size: 14px;
		color: #6b9080;
		line-height: 1.45;
	}

	.sub-price {
		font-size: 19px;
		font-weight: 900;
		color: #2f3038;
		margin-bottom: 4px;
	}

	.sub-interval {
		font-size: 14px;
		color: #7b8790;
	}

	.status-active {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		padding: 8px 13px;
		border-radius: 999px;
		background: rgba(95, 208, 173, 0.16);
		color: #1f7a63;
		font-weight: 800;
		font-size: 14px;
	}

	.status-inactive {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		padding: 8px 13px;
		border-radius: 999px;
		background: rgba(255, 120, 120, 0.13);
		color: #a13a3a;
		font-weight: 800;
		font-size: 14px;
	}

	.subscription-separator {
		height: 1px;
		background: rgba(95, 208, 173, 0.14);
		margin: 22px 0;
	}

	/* ---------- ABOÜBERSICHT INTERVAL CARDS ---------- */

	.interval-heading {
		font-size: 18px;
		font-weight: 900;
		color: #054033;
		margin-bottom: 12px;
	}

	.interval-card {
		background: rgba(255, 255, 255, 0.78);
		border: 1px solid rgba(95, 208, 173, 0.18);
		border-radius: 26px;
		padding: 22px;
		margin-bottom: 16px;
		box-shadow: 0 14px 34px rgba(31, 122, 99, 0.07);
		backdrop-filter: blur(12px);
		transition: transform 0.22s ease, box-shadow 0.22s ease, border 0.22s ease;
	}

	.interval-card:hover {
		transform: translateY(-4px);
		box-shadow: 0 20px 45px rgba(31, 122, 99, 0.13);
		border: 1px solid rgba(95, 208, 173, 0.34);
	}

	.interval-label {
		font-size: 14px;
		font-weight: 800;
		color: #6b9080;
		margin-bottom: 4px;
	}

	.interval-value {
		font-size: 25px;
		font-weight: 900;
		color: #1b5e54;
		letter-spacing: -0.5px;
	}

	/* ---------- PROGRESS BAR ---------- */

	.progress-track {
		width: 100%;
		height: 11px;
		background: rgba(95, 208, 173, 0.12);
		border-radius: 999px;
		overflow: hidden;
		margin-top: 12px;
	}

	.progress-fill {
		height: 100%;
		border-radius: 999px;
		background: linear-gradient(90deg, #5fd0ad, #1f7a63);
	}

	.progress-fill-warning {
		height: 100%;
		border-radius: 999px;
		background: linear-gradient(90deg, #ffc857, #d99200);
	}

	.progress-fill-complete {
		height: 100%;
		border-radius: 999px;
		background: linear-gradient(90deg, #1f7a63, #054033);
	}

	/* ---------- EDIT BOXES ---------- */

	.inline-edit-box {
		background:
			linear-gradient(135deg, rgba(232, 255, 245, 0.85), rgba(255, 255, 255, 0.72));
		border: 1px solid rgba(95, 208, 173, 0.2);
		border-radius: 22px;
		padding: 20px;
		margin-top: 18px;
		box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.42);
	}

	.inline-edit-title {
		font-size: 18px;
		font-weight: 900;
		color: #054033;
		margin-bottom: 10px;
	}

	.edit-box {
		background:
			linear-gradient(135deg, rgba(232, 255, 245, 0.95), rgba(255, 255, 255, 0.78));
		border: 1px solid rgba(95, 208, 173, 0.2);
		border-radius: 28px;
		padding: 24px 28px;
		margin-bottom: 24px;
		box-shadow: 0 18px 45px rgba(31, 122, 99, 0.08);
	}

	.edit-title {
		font-size: 25px;
		font-weight: 900;
		color: #054033;
		margin-bottom: 6px;
	}

	.edit-subtitle {
		font-size: 14px;
		color: #52796f;
	}

	/* ---------- EMPTY STATE ---------- */

	.empty-state {
		background: rgba(255, 255, 255, 0.72);
		border: 1px dashed rgba(95, 208, 173, 0.42);
		border-radius: 24px;
		padding: 30px;
		text-align: center;
		color: #52796f;
		margin-top: 12px;
	}

	.empty-title {
		font-size: 21px;
		font-weight: 900;
		color: #054033;
		margin-bottom: 6px;
	}

	/* ---------- DIVIDER ---------- */

	hr {
		border-color: rgba(95, 208, 173, 0.18) !important;
		margin-top: 2rem !important;
		margin-bottom: 2rem !important;
	}

	/* ---------- RESPONSIVE ---------- */

	@media (max-width: 800px) {
		h1 {
			font-size: 42px !important;
		}

		.page-intro {
			padding: 24px;
		}

		div[data-testid="stMetric"] [data-testid="stMetricValue"] {
			font-size: 23px !important;
		}
	}
	</style>
	""", unsafe_allow_html=True)


def render_page_intro(title, text):
	st.markdown(
		f"""
		<div class="page-intro">
			<div class="page-intro-title">{title}</div>
			<div class="page-intro-text">
				{text}
			</div>
		</div>
		""",
		unsafe_allow_html=True
	)


def render_section_title(title, subtitle=None):
	st.markdown(
		f'<div class="section-title">{title}</div>',
		unsafe_allow_html=True
	)

	if subtitle:
		st.markdown(
			f'<div class="section-subtitle">{subtitle}</div>',
			unsafe_allow_html=True
		)


def render_empty_state(title, text):
	st.markdown(
		f"""
		<div class="empty-state">
			<div class="empty-title">{title}</div>
			<div>{text}</div>
		</div>
		""",
		unsafe_allow_html=True
	)


def render_separator(class_name):
	st.markdown(
		f'<div class="{class_name}"></div>',
		unsafe_allow_html=True
	)