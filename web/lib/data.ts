import fs from 'fs';
import path from 'path';
import { Candidate, ModelMetrics } from './types';

const DATA_DIR = path.join(process.cwd(), 'public/data');

export async function getCandidates(): Promise<Candidate[]> {
  const dataPath = path.join(DATA_DIR, 'candidates.json');
  try {
    if (!fs.existsSync(dataPath)) {
      return [];
    }
    const fileContent = fs.readFileSync(dataPath, 'utf8');
    return JSON.parse(fileContent) as Candidate[];
  } catch (error) {
    console.error('Error loading candidates:', error);
    return [];
  }
}

export async function getCandidateById(id: string): Promise<Candidate | null> {
  try {
    const candidates = await getCandidates();
    return candidates.find((c) => c.id.toLowerCase() === id.toLowerCase()) || null;
  } catch (error) {
    console.error(`Error loading candidate by id ${id}:`, error);
    return null;
  }
}

export async function getMetrics(): Promise<ModelMetrics> {
  const dataPath = path.join(DATA_DIR, 'metrics.json');
  try {
    if (!fs.existsSync(dataPath)) {
      return {};
    }
    const fileContent = fs.readFileSync(dataPath, 'utf8');
    return JSON.parse(fileContent) as ModelMetrics;
  } catch (error) {
    console.error('Error loading metrics:', error);
    return {};
  }
}
