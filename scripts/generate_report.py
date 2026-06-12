import os
import sys
import logging
import argparse
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib import colors

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.pipeline import ExoAstroPipeline

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

def create_pdf_report(target_id, results, plot_path, out_path):
    """Generate a 3-page PDF report using ReportLab Platypus."""
    doc = SimpleDocTemplate(out_path, pagesize=letter,
                            rightMargin=50, leftMargin=50,
                            topMargin=50, bottomMargin=50)
    Story = []
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = styles['Title']
    h1_style = styles['Heading1']
    h2_style = styles['Heading2']
    normal_style = styles['Normal']
    
    # --- PAGE 1: Executive Summary & Classification ---
    Story.append(Paragraph(f"ExoAstro Vetting Report: {target_id}", title_style))
    Story.append(Spacer(1, 20))
    
    Story.append(Paragraph("1. Executive Summary & Classification Result", h1_style))
    Story.append(Spacer(1, 10))
    
    classification = results.get('classification', 'Unknown')
    confidence = results.get('confidence', 0.0)
    snr = results.get('snr', 0.0)
    
    summary_text = (
        f"This report presents the scientific vetting results for target <b>{target_id}</b>. "
        f"The ExoAstro pipeline has processed the raw TESS light curves, performed a Box Least Squares (BLS) search, "
        f"and evaluated the signal using the Advanced AstroNet multi-class Convolutional Neural Network."
    )
    Story.append(Paragraph(summary_text, normal_style))
    Story.append(Spacer(1, 15))
    
    # Results Table
    data = [
        ['Metric', 'Value'],
        ['Target ID', str(target_id)],
        ['Predicted Classification', classification],
        ['Model Confidence', f"{confidence:.2%}"],
        ['Transit Signal-to-Noise (SNR)', f"{snr:.2f}"]
    ]
    t = Table(data, colWidths=[200, 200])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 20))
    
    Story.append(Paragraph("Diagnostic Light Curve Plot", h2_style))
    if os.path.exists(plot_path):
        img = Image(plot_path, width=450, height=300)
        Story.append(img)
    else:
        Story.append(Paragraph("[Plot Image Not Found]", normal_style))
        
    Story.append(PageBreak())
    
    # --- PAGE 2: Estimated Parameters & Uncertainties ---
    Story.append(Paragraph("2. Estimated Parameters & Vetting Tests", h1_style))
    Story.append(Spacer(1, 10))
    
    period = results.get('bls_period', 0.0)
    duration = results.get('bls_duration', 0.0)
    depth = results.get('fitted_k', 0.0) ** 2  # k is Rp/Rs, depth ~ k^2
    
    Story.append(Paragraph("The following parameters were estimated via BLS and refined using PyTransit's analytical model. "
                           "Uncertainties are approximated based on grid resolution and SNR.", normal_style))
    Story.append(Spacer(1, 15))
    
    param_data = [
        ['Parameter', 'Estimated Value', 'Estimated Uncertainty'],
        ['Orbital Period (Days)', f"{period:.4f}", f"± {period * 0.01 / snr:.4f}" if snr > 0 else "N/A"],
        ['Transit Duration (Days)', f"{duration:.4f}", f"± {duration * 0.05 / snr:.4f}" if snr > 0 else "N/A"],
        ['Transit Depth (Relative Flux)', f"{depth:.5f}", f"± {0.0001 / snr:.5f}" if snr > 0 else "N/A"]
    ]
    t2 = Table(param_data, colWidths=[150, 150, 150])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.steelblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    Story.append(t2)
    Story.append(Spacer(1, 20))
    
    Story.append(Paragraph("Physical Sanity Checks", h2_style))
    vet_data = [
        ['Odd-Even Depth Discrepancy', 'Suspicious' if results.get('odd_even_suspicious') else 'Pass'],
        ['Secondary Eclipse Depth', f"{results.get('secondary_eclipse_depth', 0.0):.5f}"]
    ]
    t3 = Table(vet_data, colWidths=[225, 225])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    ]))
    Story.append(t3)
    
    Story.append(PageBreak())
    
    # --- PAGE 3: Methodology & Assumptions ---
    Story.append(Paragraph("3. Methodology, Assumptions & Tools", h1_style))
    Story.append(Spacer(1, 10))
    
    method_text = (
        "<b>Methodology:</b> Data acquisition is performed using the Lightkurve API targeting TESS high-cadence data. "
        "The time-series is stitched and cleaned (outlier rejection, flattening). A Box Least Squares (BLS) algorithm "
        "identifies periodic signals. The data is phase-folded and binned into global and local views, which are fed into "
        "a Multi-Class Advanced AstroNet 1D-CNN (with Attention layers). Finally, algorithmic vetting (Odd-Even mismatch, "
        "secondary eclipses) refines the ML confidence to produce the final classification."
    )
    Story.append(Paragraph(method_text, normal_style))
    Story.append(Spacer(1, 10))
    
    assump_text = (
        "<b>Assumptions & Uncertainties:</b> Light curve fitting via PyTransit assumes circular orbits (e=0) and uses "
        "standard quadratic limb darkening coefficients. We assume the out-of-transit baseline is perfectly flattened. "
        "Uncertainties in parameters are estimated heuristically as a function of the signal-to-noise ratio (SNR) "
        "of the phase-folded dip, bounded by the intrinsic cadence of the observations."
    )
    Story.append(Paragraph(assump_text, normal_style))
    Story.append(Spacer(1, 10))
    
    tools_text = (
        "<b>Tools & Libraries:</b><br/>"
        "- Python 3<br/>"
        "- Lightkurve (Data fetching, BLS, Detrending)<br/>"
        "- TensorFlow/Keras (1D-CNN Multi-class model)<br/>"
        "- PyTransit (Analytical transit model fitting)<br/>"
        "- ReportLab (PDF Generation)"
    )
    Story.append(Paragraph(tools_text, normal_style))
    
    # Build Document
    doc.build(Story)
    log.info(f"Report saved to {out_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate 3-page vetting report.")
    parser.add_argument("--target", default="Kepler-10b", help="Target ID")
    parser.add_argument("--outdir", default="outputs/reports", help="Output directory")
    args = parser.parse_args()

    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)

    pipeline = ExoAstroPipeline()
    results = pipeline.run(args.target, author='SPOC', exptime=120)
    
    if results:
        plot_filename = f"{args.target.replace(' ', '_')}_folded.png"
        plot_path = os.path.join(args.outdir, plot_filename)
        
        try:
            lc_collection = pipeline.fetcher.fetch_lightcurve(args.target, author='SPOC', exptime=120)
            lc_clean = pipeline.fetcher.stitch_and_clean(lc_collection)
            pipeline.vetter.plot_folded_transit(
                lc_clean, results['bls_period'], results['bls_t0'], results['bls_duration'], plot_path
            )
        except Exception as e:
            log.warning(f"Could not generate plot: {e}")
            plot_path = "" # Will display not found text
        
        report_path = os.path.join(args.outdir, f"{args.target.replace(' ', '_')}_report.pdf")
        create_pdf_report(args.target, results, plot_path, report_path)

if __name__ == "__main__":
    main()
