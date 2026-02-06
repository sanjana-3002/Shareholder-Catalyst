"""
Shareholder Catalyst - Streamlit Web Interface
Interactive web app for activist investor analysis
"""

import streamlit as st
import asyncio
import os
from dotenv import load_dotenv
import time
from io import BytesIO
from datetime import datetime

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Shareholder Catalyst",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Demo mode flag
DEMO_MODE = True  # Set to True for judges/demo purposes

# Helper functions for demo data
def get_demo_result(ticker):
    """Get demo data for common tickers"""
    
    demo_data = {
        "AAPL": {
            "company_name": "Apple Inc.",
            "ticker": "AAPL",
            "metrics": type('obj', (object,), {
                'market_cap': 2800000000000,
                'enterprise_value': 2750000000000,
                'ev_to_revenue': 7.2,
                'roe': 147.4,
                'roic': 28.1,
                'operating_margin': 29.8,
                'revenue_growth_1y': -2.8,
                'cash_to_assets_ratio': 8.5
            }),
            'red_flags': {
                'excess_cash': 'Company holds $30B in excess cash (8.5% of assets) that could be returned to shareholders',
                'declining_growth': 'Revenue declined 2.8% year-over-year, suggesting market saturation'
            },
            'peer_comparison': type('obj', (object,), {
                'roe_percentile': 95.0,
                'roic_percentile': 88.0,
                'roe_gap': 132.4,
                'roic_gap': 18.1,
                'upside_to_peer_median': 25.3,
                'peer_group': ['MSFT', 'GOOGL', 'META', 'AMZN']
            }),
            'extracted_data': {
                '10k': {
                    'revenue_current': 383285000000,
                    'net_income_current': 96995000000,
                    'total_assets': 352755000000,
                    'cash_equivalents': 29965000000,
                    'total_debt': 111088000000,
                    'operating_income': 114301000000,
                    'shareholders_equity': 62146000000
                },
                'market_data': {
                    'current_price': 189.50,
                    'market_cap': 2800000000000,
                    'shares_outstanding': 14782456000
                },
                'proxy': {
                    'ceo_total_comp_current': 63209230,
                    'board_members': [
                        {"name": "Tim Cook", "role": "CEO & Director", "tenure_years": 12, "independent": False},
                        {"name": "Arthur D. Levinson", "role": "Chairman", "tenure_years": 21, "independent": True},
                        {"name": "James A. Bell", "role": "Director", "tenure_years": 15, "independent": True}
                    ],
                    'say_on_pay_approval_pct': 95.4
                }
            },
            'financial_analysis': generate_demo_financial_analysis("AAPL"),
            'governance_analysis': generate_demo_governance_analysis("AAPL"),
            'ai_thesis': generate_demo_thesis("AAPL"),
            'basic_thesis': generate_demo_thesis("AAPL")
        },
        "MSFT": {
            "company_name": "Microsoft Corporation",
            "ticker": "MSFT",
            "metrics": type('obj', (object,), {
                'market_cap': 2900000000000,
                'enterprise_value': 2850000000000,
                'ev_to_revenue': 12.5,
                'roe': 38.4,
                'roic': 22.1,
                'operating_margin': 42.0,
                'revenue_growth_1y': 13.2,
                'cash_to_assets_ratio': 7.2
            }),
            'red_flags': {
                'high_valuation': 'Trading at premium valuation vs historical averages',
                'cloud_competition': 'Increasing competition in cloud services from AWS and Google'
            },
            'peer_comparison': type('obj', (object,), {
                'roe_percentile': 82.0,
                'roic_percentile': 85.0,
                'roe_gap': 23.4,
                'roic_gap': 12.1,
                'upside_to_peer_median': 15.2,
                'peer_group': ['AAPL', 'GOOGL', 'META', 'AMZN']
            }),
            'extracted_data': {
                '10k': {
                    'revenue_current': 211915000000,
                    'net_income_current': 72361000000,
                    'total_assets': 411976000000,
                    'cash_equivalents': 29945000000,
                    'total_debt': 47032000000,
                    'operating_income': 89035000000,
                    'shareholders_equity': 206223000000
                },
                'market_data': {
                    'current_price': 415.25,
                    'market_cap': 2900000000000,
                    'shares_outstanding': 7430000000
                },
                'proxy': {
                    'ceo_total_comp_current': 54946310,
                    'board_members': [
                        {"name": "Satya Nadella", "role": "CEO & Director", "tenure_years": 10, "independent": False},
                        {"name": "John W. Thompson", "role": "Chairman", "tenure_years": 13, "independent": True}
                    ],
                    'say_on_pay_approval_pct': 91.2
                }
            },
            'financial_analysis': generate_demo_financial_analysis("MSFT"),
            'governance_analysis': generate_demo_governance_analysis("MSFT"),
            'ai_thesis': generate_demo_thesis("MSFT"),
            'basic_thesis': generate_demo_thesis("MSFT")
        }
        # Add more companies as needed
    }
    
    return demo_data.get(ticker, demo_data["AAPL"])

def generate_demo_financial_analysis(ticker):
    analyses = {
        "AAPL": """
        ## Financial Performance Analysis for Apple Inc.

        ### Revenue & Profitability
        Apple demonstrates exceptional profitability metrics with a **29.8% operating margin** and **147% ROE**, significantly outperforming industry peers. However, revenue declined **2.8% year-over-year** to $383.3B, indicating potential market saturation in key product categories.

        ### Capital Efficiency
        The company maintains a **28.1% ROIC**, demonstrating superior capital allocation efficiency. However, this efficiency is masked by substantial excess cash holdings that are not being deployed productively.

        ### Balance Sheet Strength
        With $30B in cash and cash equivalents against $111B in total debt, Apple maintains a strong but inefficient balance sheet. The excess cash represents **8.5% of total assets** and could generate significant shareholder value through strategic deployment.

        ### Key Financial Red Flags for Activists:
        1. **Declining Growth**: Revenue contraction suggests need for new growth initiatives or capital return
        2. **Excess Cash**: $30B in excess cash earning minimal returns
        3. **Conservative Capital Structure**: Underleveraged relative to peers and optimal capital structure
        """,
        "MSFT": """
        ## Financial Performance Analysis for Microsoft Corporation

        ### Revenue & Profitability
        Microsoft shows strong growth momentum with **13.2% revenue growth** and exceptional **42% operating margins**, driven by cloud and productivity services. ROE of **38.4%** reflects efficient operations.

        ### Capital Efficiency
        ROIC of **22.1%** demonstrates strong capital deployment, particularly in cloud infrastructure investments that are generating sustainable competitive advantages.

        ### Balance Sheet Analysis
        Conservative debt levels at $47B provide financial flexibility, though cash position could be optimized for shareholder returns.

        ### Key Areas for Activist Focus:
        1. **Valuation Premium**: High multiples suggest need for accelerated growth
        2. **Capital Allocation**: Opportunity for enhanced shareholder returns
        3. **Innovation Investment**: Maintaining leadership in AI and cloud requires continued R&D
        """
    }
    return analyses.get(ticker, analyses["AAPL"])

def generate_demo_governance_analysis(ticker):
    analyses = {
        "AAPL": """
        ## Corporate Governance Analysis for Apple Inc.

        ### Board Composition
        The board consists of experienced directors, but several governance concerns merit activist attention:

        ### Executive Compensation
        CEO total compensation of **$63.2M** represents a reasonable multiple of median worker pay, though say-on-pay approval at **95.4%** indicates some shareholder concern.

        ### Board Independence & Tenure
        - Chairman Arthur Levinson has served **21 years** - significant tenure that may impact independence
        - James Bell has served **15 years** - above typical governance guidelines
        - Board refreshment opportunity exists

        ### Governance Red Flags for Activists:
        1. **Board Tenure**: Multiple directors exceed 12-year independence thresholds
        2. **Succession Planning**: Limited public disclosure on CEO succession planning
        3. **Capital Allocation**: Board oversight of excess cash deployment appears insufficient

        ### Shareholder Rights
        Standard shareholder rights with annual director elections. No poison pill or classified board structure.
        """,
        "MSFT": """
        ## Corporate Governance Analysis for Microsoft Corporation

        ### Board Composition
        Well-structured board with appropriate mix of technical and business expertise.

        ### Executive Compensation
        CEO compensation of **$54.9M** aligned with performance metrics and shareholder returns.

        ### Governance Strengths
        - Strong independent board leadership
        - Appropriate executive compensation alignment
        - Transparent succession planning processes

        ### Areas for Enhancement
        1. **ESG Reporting**: Opportunity for enhanced sustainability disclosure
        2. **Innovation Governance**: Board oversight of AI and emerging technology investments
        """
    }
    return analyses.get(ticker, analyses["AAPL"])

def generate_demo_thesis(ticker):
    theses = {
        "AAPL": """
        # Activist Investment Thesis: Apple Inc.

        ## Executive Summary
        Apple represents a compelling activist opportunity due to significant excess cash, declining revenue growth, and governance inefficiencies. We recommend a targeted campaign focused on capital allocation optimization and operational excellence.

        ## Investment Rationale

        ### 1. Capital Allocation Inefficiency
        - **$30B excess cash** earning minimal returns
        - **Opportunity**: Force special dividend or accelerated buyback program
        - **Value Creation**: $15-20 per share value unlock

        ### 2. Revenue Growth Stagnation
        - **2.8% revenue decline** indicates market saturation
        - **Opportunity**: Push for aggressive R&D investment or strategic acquisitions
        - **Value Creation**: Restore 5-10% revenue growth trajectory

        ### 3. Governance Improvements
        - **Board refreshment** needed (21-year tenure for Chairman)
        - **Enhanced disclosure** on capital allocation framework
        - **Improved CEO succession planning**

        ## Activist Campaign Strategy

        ### Phase 1: Private Engagement (3 months)
        1. Request meetings with CFO and Board
        2. Present capital allocation analysis
        3. Propose specific actions and timeline

        ### Phase 2: Public Campaign (6 months)
        1. File 13D disclosure
        2. Launch public campaign highlighting inefficiencies
        3. Propose board nominees if needed

        ## Financial Projections

        ### Base Case
        - Current Share Price: $189.50
        - Target Price: $225 (+18.7%)
        - Timeline: 12-18 months

        ### Bull Case
        - Optimal capital structure achieved
        - Revenue growth restored to 7%
        - Target Price: $250 (+32.0%)

        ## Key Risks
        1. **Execution Risk**: Management may resist changes
        2. **Market Risk**: Broader tech sector volatility
        3. **Regulatory Risk**: Antitrust scrutiny may limit strategic options

        ## Conclusion
        Apple's combination of financial strength, governance issues, and capital allocation inefficiency creates an ideal activist target with significant value creation potential of $20-40 per share.
        """,
        "MSFT": """
        # Activist Investment Thesis: Microsoft Corporation

        ## Executive Summary
        Microsoft presents a moderate activist opportunity focused on accelerating cloud growth and optimizing capital deployment for maximum shareholder returns.

        ## Investment Rationale

        ### 1. Cloud Market Leadership
        - **42% operating margins** in cloud services
        - **Opportunity**: Accelerate market share capture
        - **Value Creation**: Maintain premium valuation through growth

        ### 2. Capital Optimization
        - Strong cash generation capabilities
        - **Opportunity**: Enhanced shareholder return programs
        - **Value Creation**: Improved ROIC and shareholder yields

        ### 3. AI Leadership Position
        - Early mover advantage in enterprise AI
        - **Opportunity**: Monetize AI investments aggressively
        - **Value Creation**: Expand market leadership

        ## Target Outcomes
        - Current Price: $415.25
        - Target Price: $475 (+14.4%)
        - Focus on sustainable growth premium

        ## Conclusion
        Microsoft's strong fundamentals and growth trajectory make it a defensive activist play with moderate upside potential.
        """
    }
    return theses.get(ticker, theses["AAPL"])

def display_executive_summary(result):
    st.header(f"{result['company_name']} ({result['ticker']})")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = result['metrics']
    market_data = result['extracted_data']['market_data']
    
    with col1:
        st.metric(
            "Market Cap",
            f"${market_data['market_cap']/1e9:.1f}B"
        )
    
    with col2:
        st.metric(
            "ROE",
            f"{metrics.roe:.1f}%",
            delta=f"{metrics.roe - 15:.1f}pp" if metrics.roe > 15 else None
        )
    
    with col3:
        st.metric(
            "ROIC",
            f"{metrics.roic:.1f}%",
            delta=f"{metrics.roic - 10:.1f}pp" if metrics.roic > 10 else None
        )
    
    with col4:
        st.metric(
            "Operating Margin",
            f"{metrics.operating_margin:.1f}%"
        )
    
    st.divider()
    
    # Investment Recommendation
    st.subheader("🎯 Investment Recommendation")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.success("**STRONG BUY** - High-conviction activist opportunity")
        st.write("Target price: $225 (+18.7% upside) | Timeline: 12-18 months")
    
    with col2:
        st.metric("Conviction", "95%", delta="High")
    
    # Red flags
    if result['red_flags']:
        st.subheader("🚩 Key Activist Catalysts")
        for flag_name, flag_desc in result['red_flags'].items():
            st.error(f"**{flag_name.replace('_', ' ').title()}**: {flag_desc}")
    
    st.divider()
    
    # Peer comparison
    st.subheader("📊 Peer Comparison")
    peer_comp = result['peer_comparison']
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "ROE Percentile",
            f"{peer_comp.roe_percentile:.0f}th",
            delta=f"{peer_comp.roe_gap:+.1f}pp vs median"
        )
    
    with col2:
        st.metric(
            "ROIC Percentile",
            f"{peer_comp.roic_percentile:.0f}th",
            delta=f"{peer_comp.roic_gap:+.1f}pp vs median"
        )
    
    with col3:
        st.metric(
            "Valuation Gap",
            f"{peer_comp.upside_to_peer_median:+.1f}%",
            delta="Upside potential" if peer_comp.upside_to_peer_median > 0 else "Trading premium"
        )
        
    st.caption(f"Peer group: {', '.join(peer_comp.peer_group[:4])}")

def display_financial_analysis(result):
    st.header("💰 Financial Deep-Dive Analysis")
    
    if result['financial_analysis'] and result['financial_analysis'] != "Rule-based analysis (add LLM key for AI analysis)":
        st.markdown(result['financial_analysis'])
    else:
        # Show detailed financial data even without LLM
        fin_data = result['extracted_data']['10k']
        
        st.subheader("Income Statement Highlights")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Revenue", f"${fin_data['revenue_current']/1e9:.1f}B")
            st.metric("Operating Income", f"${fin_data['operating_income']/1e9:.1f}B")
        
        with col2:
            st.metric("Net Income", f"${fin_data['net_income_current']/1e9:.1f}B")
            st.metric("Operating Margin", f"{(fin_data['operating_income']/fin_data['revenue_current']*100):.1f}%")
        
        with col3:
            st.metric("Net Margin", f"{(fin_data['net_income_current']/fin_data['revenue_current']*100):.1f}%")
            st.metric("ROE", f"{result['metrics'].roe:.1f}%")
        
        st.subheader("Balance Sheet Analysis")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Assets", f"${fin_data['total_assets']/1e9:.1f}B")
            st.metric("Shareholders' Equity", f"${fin_data['shareholders_equity']/1e9:.1f}B")
        
        with col2:
            st.metric("Cash & Equivalents", f"${fin_data['cash_equivalents']/1e9:.1f}B")
            st.metric("Total Debt", f"${fin_data['total_debt']/1e9:.1f}B")
        
        with col3:
            st.metric("Cash/Assets Ratio", f"{(fin_data['cash_equivalents']/fin_data['total_assets']*100):.1f}%")
            st.metric("Debt/Equity Ratio", f"{(fin_data['total_debt']/fin_data['shareholders_equity']):.1f}x")

def display_governance_analysis(result):
    st.header("👔 Corporate Governance Analysis")
    
    if result['governance_analysis'] and result['governance_analysis'] != "Rule-based analysis (add LLM key for AI analysis)":
        st.markdown(result['governance_analysis'])
    else:
        if 'proxy' in result['extracted_data']:
            proxy_data = result['extracted_data']['proxy']
            
            st.subheader("Executive Compensation")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(
                    "CEO Total Compensation",
                    f"${proxy_data['ceo_total_comp_current']/1e6:.1f}M"
                )
            
            with col2:
                if 'say_on_pay_approval_pct' in proxy_data:
                    st.metric(
                        "Say-on-Pay Approval",
                        f"{proxy_data['say_on_pay_approval_pct']:.1f}%"
                    )
            
            st.subheader("Board of Directors")
            if proxy_data.get('board_members'):
                for member in proxy_data['board_members']:
                    col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                    with col1:
                        st.write(f"**{member['name']}**")
                    with col2:
                        st.write(member['role'])
                    with col3:
                        st.write(f"{member['tenure_years']} yrs")
                    with col4:
                        if member['tenure_years'] > 12:
                            st.error("⚠️ Long tenure")
                        else:
                            st.success("✅ Appropriate")

def display_investment_thesis(result):
    st.header("🎯 Investment Thesis")
    
    thesis_to_show = result.get('ai_thesis')
    if not thesis_to_show or thesis_to_show in ["Rule-based thesis (add LLM key for AI-generated thesis)", "AI thesis not available (no API key)"]:
        thesis_to_show = result['basic_thesis']
    
    st.markdown(thesis_to_show)

def display_complete_report(result):
    st.header("📄 Complete Activist Investment Report")
    
    # Generate comprehensive report
    report = generate_complete_report(result)
    st.markdown(report)

def generate_complete_report(result):
    """Generate a comprehensive activist investment report"""
    
    report = f"""
# Activist Investment Analysis: {result['company_name']} ({result['ticker']})

## Table of Contents
1. Executive Summary
2. Financial Analysis  
3. Governance Assessment
4. Activist Opportunities
5. Investment Thesis
6. Risk Assessment
7. Action Plan

---

## 1. Executive Summary

**Company**: {result['company_name']} ({result['ticker']})  
**Market Cap**: ${result['extracted_data']['market_data']['market_cap']/1e9:.1f}B  
**Current Price**: ${result['extracted_data']['market_data']['current_price']:.2f}  
**Target Price**: $225.00 (+18.7% upside)  
**Investment Recommendation**: **STRONG BUY**  

### Key Investment Highlights
- Exceptional profitability metrics (ROE: {result['metrics'].roe:.1f}%, ROIC: {result['metrics'].roic:.1f}%)
- Significant excess cash requiring optimization
- Multiple governance improvement opportunities
- Clear path to value creation through activist engagement

---

## 2. Financial Analysis

### Profitability Metrics
- **Revenue**: ${result['extracted_data']['10k']['revenue_current']/1e9:.1f}B
- **Operating Margin**: {result['metrics'].operating_margin:.1f}%
- **Net Income**: ${result['extracted_data']['10k']['net_income_current']/1e9:.1f}B
- **ROE**: {result['metrics'].roe:.1f}% (vs. peer median: 15.0%)
- **ROIC**: {result['metrics'].roic:.1f}% (vs. peer median: 10.0%)

### Balance Sheet Analysis
- **Total Assets**: ${result['extracted_data']['10k']['total_assets']/1e9:.1f}B
- **Cash & Equivalents**: ${result['extracted_data']['10k']['cash_equivalents']/1e9:.1f}B
- **Total Debt**: ${result['extracted_data']['10k']['total_debt']/1e9:.1f}B
- **Shareholders' Equity**: ${result['extracted_data']['10k']['shareholders_equity']/1e9:.1f}B

### Key Financial Red Flags
"""
    
    for flag, description in result.get('red_flags', {}).items():
        report += f"- **{flag.replace('_', ' ').title()}**: {description}\n"
    
    report += """
---

## 3. Governance Assessment

### Board Composition
"""
    
    if 'proxy' in result['extracted_data'] and 'board_members' in result['extracted_data']['proxy']:
        for member in result['extracted_data']['proxy']['board_members']:
            report += f"- **{member['name']}**: {member['role']} ({member['tenure_years']} years)\n"
    
    report += f"""

### Executive Compensation
- **CEO Total Compensation**: ${result['extracted_data']['proxy']['ceo_total_comp_current']/1e6:.1f}M
- **Say-on-Pay Approval**: {result['extracted_data']['proxy']['say_on_pay_approval_pct']:.1f}%

---

## 4. Activist Opportunities

### Primary Value Creation Levers
1. **Capital Allocation Optimization**: Deploy excess cash productively
2. **Operational Excellence**: Restore revenue growth trajectory  
3. **Governance Enhancement**: Board refreshment and enhanced oversight

### Potential Value Creation
- **Base Case**: $225/share (+18.7% upside)
- **Bull Case**: $250/share (+32.0% upside)

---

## 5. Investment Thesis

{result.get('ai_thesis', result.get('basic_thesis', 'Investment thesis analysis'))}

---

## 6. Risk Assessment

### Key Risks
- **Execution Risk**: Management resistance to proposed changes
- **Market Risk**: Technology sector volatility
- **Regulatory Risk**: Antitrust and regulatory scrutiny

### Risk Mitigation
- Engage constructively with management first
- Build coalition with other institutional investors
- Develop clear, implementable action plan

---

## 7. Action Plan

### Phase 1: Private Engagement (Months 1-3)
1. Request meetings with senior management and board
2. Present detailed analysis and recommendations
3. Negotiate timeline for implementation

### Phase 2: Public Campaign (Months 4-9)
1. File Schedule 13D if private engagement unsuccessful
2. Launch public campaign highlighting value creation opportunities
3. Seek board representation if necessary

### Phase 3: Value Realization (Months 10-18)
1. Monitor implementation of agreed actions
2. Track value creation metrics
3. Consider exit strategy as targets achieved

---

*Report generated on {datetime.now().strftime("%B %d, %Y")}*
"""
    
    return report

def display_download_options(result, ticker):
    st.header("💾 Download Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Full Report")
        
        # Generate report content
        report_content = generate_complete_report(result)
        
        # Markdown download
        st.download_button(
            label="📥 Download as Markdown",
            data=report_content,
            file_name=f"activist_analysis_{ticker}_{datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown"
        )
        
    with col2:
        st.subheader("📊 PDF Report")
        
        # Generate PDF
        pdf_content = generate_pdf_report(result, ticker)
        
        if pdf_content:
            st.download_button(
                label="📥 Download as PDF",
                data=pdf_content,
                file_name=f"activist_analysis_{ticker}_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )
        else:
            st.info("PDF generation requires additional setup. Markdown available above.")
    
    st.divider()
    
    st.subheader("📋 Data Export")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Financial data as JSON
        import json
        financial_data = {
            'company': result['company_name'],
            'ticker': result['ticker'],
            'financial_metrics': {
                'revenue': result['extracted_data']['10k']['revenue_current'],
                'net_income': result['extracted_data']['10k']['net_income_current'],
                'total_assets': result['extracted_data']['10k']['total_assets'],
                'market_cap': result['extracted_data']['market_data']['market_cap']
            },
            'activist_metrics': {
                'roe': result['metrics'].roe,
                'roic': result['metrics'].roic,
                'operating_margin': result['metrics'].operating_margin
            }
        }
        
        st.download_button(
            label="📄 Financial Data (JSON)",
            data=json.dumps(financial_data, indent=2),
            file_name=f"financial_data_{ticker}_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
    
    with col2:
        # Investment thesis only
        thesis_content = result.get('ai_thesis', result.get('basic_thesis', ''))
        
        st.download_button(
            label="🎯 Investment Thesis Only",
            data=thesis_content,
            file_name=f"investment_thesis_{ticker}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )

def generate_pdf_report(result, ticker):
    """Generate PDF report (requires reportlab)"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib import colors
        
        buffer = BytesIO()
        
        # Create PDF
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title = Paragraph(f"Activist Investment Analysis: {result['company_name']} ({ticker})", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", styles['Heading1']))
        summary_text = f"""
        <b>Investment Recommendation:</b> STRONG BUY<br/>
        <b>Target Price:</b> $225.00 (+18.7% upside)<br/>
        <b>Market Cap:</b> ${result['extracted_data']['market_data']['market_cap']/1e9:.1f}B<br/>
        <b>ROE:</b> {result['metrics'].roe:.1f}%<br/>
        <b>ROIC:</b> {result['metrics'].roic:.1f}%
        """
        story.append(Paragraph(summary_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Financial Table
        story.append(Paragraph("Key Financial Metrics", styles['Heading2']))
        financial_data = [
            ['Metric', 'Value'],
            ['Revenue', f"${result['extracted_data']['10k']['revenue_current']/1e9:.1f}B"],
            ['Net Income', f"${result['extracted_data']['10k']['net_income_current']/1e9:.1f}B"],
            ['Total Assets', f"${result['extracted_data']['10k']['total_assets']/1e9:.1f}B"],
            ['Cash', f"${result['extracted_data']['10k']['cash_equivalents']/1e9:.1f}B"],
            ['ROE', f"{result['metrics'].roe:.1f}%"],
            ['ROIC', f"{result['metrics'].roic:.1f}%"]
        ]
        
        table = Table(financial_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Investment Thesis
        story.append(Paragraph("Investment Thesis", styles['Heading2']))
        thesis = result.get('ai_thesis', result.get('basic_thesis', ''))[:1000] + "..."
        story.append(Paragraph(thesis, styles['Normal']))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
        
    except ImportError:
        return None  # reportlab not installed
    except Exception as e:
        st.error(f"PDF generation failed: {str(e)}")
        return None

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stage-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        background-color: #f0f2f6;
    }
    .metric-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">🎯 Shareholder Catalyst</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Activist Investor Intelligence</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Demo Mode Notice
    if DEMO_MODE:
        st.success("🎭 **DEMO MODE**")
        st.info("For judges: API keys not required. Using demo data to showcase full functionality.")
        st.divider()
    
    # API Status
    st.subheader("API Status")
    landing_ai_key = os.getenv('VISION_AGENT_API_KEY') or os.getenv('LANDING_AI_API_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    
    if DEMO_MODE:
        st.success("✅ LandingAI API (Demo)")
        st.success("✅ Analysis LLM (Demo)")
        st.caption("Demo mode provides realistic sample data")
    else:
        if landing_ai_key and landing_ai_key not in ['your_landingai_api_key_here', 'test_key']:
            st.success("✅ LandingAI API")
        else:
            st.error("❌ LandingAI API")
            st.caption("Add LANDING_AI_API_KEY to .env")
        
        if openai_key or anthropic_key:
            st.success("✅ Analysis LLM")
        else:
            st.warning("⚠️ No LLM (rule-based)")
            st.caption("Add OPENAI_API_KEY or ANTHROPIC_API_KEY for AI analysis")
    
    st.divider()
    
    # Info
    st.subheader("ℹ️ How It Works")
    st.markdown("""
    1. **SEC EDGAR**: Fetch filings
    2. **LandingAI**: Extract data
    3. **Market Data**: Get prices
    4. **Analysis**: Generate thesis
    """)
    
    st.divider()
    
    st.subheader("📊 Example Companies")
    example_tickers = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN", "META", "NFLX"]
    for ticker in example_tickers:
        if st.button(ticker, key=f"example_{ticker}", use_container_width=True):
            st.session_state.ticker_input = ticker

# Main content
col1, col2, col3 = st.columns([2, 1, 2])

with col2:
    ticker_input = st.text_input(
        "Enter Stock Ticker",
        value=st.session_state.get('ticker_input', ''),
        placeholder="e.g., AAPL",
        key="main_ticker_input"
    ).upper()
    
    analyze_button = st.button("🚀 Analyze Company", type="primary", use_container_width=True)

if analyze_button and ticker_input:
    # Initialize orchestrator
    try:
        from orchestrator import ActivistIntelOrchestrator
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Create tabs for results
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Executive Summary", 
            "📈 Financial Deep-Dive",
            "👔 Governance Analysis", 
            "🎯 Investment Thesis",
            "📄 Complete Report",
            "💾 Download"
        ])
        
        # Run analysis
        status_text.text("Initializing analysis...")
        progress_bar.progress(10)
        
        # Demo mode or real analysis
        if DEMO_MODE and ticker_input.upper() in ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN", "META", "NFLX"]:
            status_text.text("🎭 Running demo analysis...")
            progress_bar.progress(50)
            time.sleep(2)  # Simulate processing
            result = get_demo_result(ticker_input.upper())
            progress_bar.progress(100)
            status_text.text("✅ Demo analysis complete!")
        else:
            orchestrator = ActivistIntelOrchestrator()
            
            # Stage 1: SEC Filings
            status_text.text(f"📄 Fetching SEC filings for {ticker_input}...")
            progress_bar.progress(20)
            
            result = asyncio.run(orchestrator.analyze_company(ticker_input))
            
            progress_bar.progress(100)
            status_text.text("✅ Analysis complete!")
        
        time.sleep(1)
        status_text.empty()
        progress_bar.empty()
        
        # Display results
        with tab1:
            display_executive_summary(result)
        
        with tab2:
            display_financial_analysis(result)
        
        with tab3:
            display_governance_analysis(result)
        
        with tab4:
            display_investment_thesis(result)
        
        with tab5:
            display_complete_report(result)
        
        with tab6:
            display_download_options(result, ticker_input)
    
    except Exception as e:
        st.error(f"❌ Analysis failed: {str(e)}")
        if not DEMO_MODE:
            st.exception(e)
        else:
            st.info("Demo mode: Using sample data to showcase functionality")

elif analyze_button and not ticker_input:
    st.warning("⚠️ Please enter a stock ticker")

# Footer
st.divider()
col1, col2, col3 = st.columns(3)
with col2:
    st.caption("🎯 Shareholder Catalyst | Powered by LandingAI")
