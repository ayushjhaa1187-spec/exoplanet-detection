import os
import sys
import logging
import argparse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.pipeline import ExoAstroPipeline

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

def create_pdf_report(target_id, results, plot_path, out_path):
    """Generate a PDF report for the exoplanet candidate."""
    c = canvas.Canvas(out_path, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 50, f"Exoplanet Vetting Report: {target_id}")

    # Results Table
    c.setFont("Helvetica", 12)
    y = height - 100
    for key, value in results.items():
        if key != 'target_id':
            c.drawString(50, y, f"{key}: {value}")
            y -= 20

    # Diagnostic Plot
    if os.path.exists(plot_path):
        img = ImageReader(plot_path)
        c.drawImage(img, 50, y - 350, width=500, preserveAspectRatio=True)

    c.showPage()
    c.save()
    log.info(f"Report saved to {out_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate vetting report.")
    parser.add_argument("--target", default="Kepler-10b", help="Target ID")
    parser.add_argument("--outdir", default="outputs/reports", help="Output directory")
    args = parser.parse_args()

    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)

    pipeline = ExoAstroPipeline()
    # Run the pipeline (using quarter=2 for speed)
    results = pipeline.run(args.target, quarter=2)
    
    if results:
        # Generate diagnostic plot
        # Need the cleaned lightcurve. Pipeline doesn't return it currently.
        # Let's refetch it or modify pipeline to return it.
        # For this demo, let's just use the plot_folded_transit inside pipeline.
        
        # Modify pipeline to save plot
        plot_filename = f"{args.target.replace(' ', '_')}_folded.png"
        plot_path = os.path.join(args.outdir, plot_filename)
        
        # Re-fetch for plotting (inefficient but works for PoC)
        lc_collection = pipeline.fetcher.fetch_lightcurve(args.target, quarter=2)
        lc_clean = pipeline.fetcher.stitch_and_clean(lc_collection)
        pipeline.vetter.plot_folded_transit(
            lc_clean, results['bls_period'], results['bls_t0'], results['bls_duration'], plot_path
        )
        
        report_path = os.path.join(args.outdir, f"{args.target.replace(' ', '_')}_report.pdf")
        create_pdf_report(args.target, results, plot_path, report_path)

if __name__ == "__main__":
    main()
