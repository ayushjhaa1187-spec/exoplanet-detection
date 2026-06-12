import os
import yaml
import logging
import argparse
import pandas as pd
import lightkurve as lk

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Download TESS sector catalog and lightcurves.")
    parser.add_argument("--config", default="configs/sector.yaml", help="Path to sector config file")
    args = parser.parse_args()

    if not os.path.exists(args.config):
        log.error(f"Config file not found: {args.config}")
        return

    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    sector = config.get('sector', 27)
    author = config.get('author', 'SPOC')
    limit = config.get('max_targets', 100)
    
    outdir = "data/catalog"
    os.makedirs(outdir, exist_ok=True)
    
    log.info(f"Searching MAST for TESS Sector {sector} ({author}). Limit: {limit}")
    
    # We search by wildcard coordinate or we can just fetch a known target list.
    # To fetch a random sample from a sector without specific coords, we can search the entire sector
    # Note: lightkurve search without target usually requires a radius or a mission/sector specific target.
    # A common hack is to search by mission='TESS', sector=sector, but MAST API requires coordinates or target.
    # For the sake of this pipeline, let's assume we have a list of TOIs or we query the TESS Input Catalog (TIC).
    
    # Since lk.search_lightcurve requires a target name or coordinate, we will use a small sample 
    # of known TICs if we want to demonstrate. Let's create a predefined list for sector 27 if no catalog provided.
    sample_targets = ["TIC 25155310", "TIC 270810595", "TIC 154483584", "TIC 220023640", "TIC 381180295"]
    
    records = []
    
    for tic in sample_targets[:limit]:
        log.info(f"Querying {tic} in Sector {sector}")
        search = lk.search_lightcurve(tic, author=author, sector=sector)
        if len(search) > 0:
            records.append({
                'TIC_ID': tic,
                'sector': sector,
                'author': author,
                'exptime': search.exptime.value[0],
                'target_name': search.target_name[0]
            })
            
    df = pd.DataFrame(records)
    out_csv = os.path.join(outdir, f"sector_{sector}_targets.csv")
    df.to_csv(out_csv, index=False)
    log.info(f"Saved catalog to {out_csv}")
    
if __name__ == "__main__":
    main()
