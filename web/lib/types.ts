export interface Candidate {
  id: string;
  targetName: string;
  astronet_score: number;
  label: string;
  bls_period: number;
  bls_t0?: number;
  bls_duration?: number;
  snr: number;
  fitted_k: number;
  odd_even_suspicious: boolean;
  secondary_eclipse_depth: number;
  status: string;
  quarter?: string;
  shortSummary?: string;
  foldedPlot?: string;
  diagnosticPlot?: string;
  transitFitPlot?: string;
}

export interface ModelMetrics {
  experimentName?: string;
  accuracy?: number;
  precision?: number;
  recall?: number;
  f1?: number;
  auc?: number;
  datasetSize?: number;
  notes?: string;
}
