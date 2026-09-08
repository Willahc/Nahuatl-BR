export interface GateStatus {
  status: string;
  closure: string;
}

export interface Counts {
  lemmas: number;
  sources: number;
  claims_total: number;
  evidence_total: number;
  integration_items: number;
}

export interface SourceDto {
  name?: string;
  institution?: string;
  url?: string;
  recommended_role?: string;
}

export interface LemmaAttestation {
  source_id?: string;
  work?: string;
  locator?: string;
  url?: string;
  mediation_level?: string;
  direct_witness_inspected?: boolean;
}

export interface LemmaReference {
  source?: string;
  work?: string;
  locator?: string;
  url?: string;
  use?: string;
}

export interface AnalysisCandidate {
  profile?: string;
  editorial_state?: string;
  modality?: string;
  confidence?: string;
  vowel_length?: string;
  saltillo?: string;
  phonemic_ipa?: string;
  phonetic_ipa?: string;
  claim_ids?: string[];
  notes?: string;
}

export interface LemmaPhonology {
  vowel_length?: string;
  saltillo?: string;
  status?: string;
  notes?: string[];
  analysis_candidate?: AnalysisCandidate;
}

export interface LemmaDto {
  id: string;
  display_form?: string;
  variety?: string;
  status?: string;
  forms: {
    source_forms: string[];
    normalized_form?: string;
    pedagogical_form?: string;
    search_keys: string[];
  };
  interpretations: string[];
  pt_br_editorial: string[];
  historical_glosses: string[];
  phonology: LemmaPhonology;
  sources: LemmaAttestation[];
  references: LemmaReference[];
  notes?: string;
  claim_ids: string[];
}

export interface PreviewData {
  schema: string;
  pipeline_version: string;
  generated_by: string;
  generated_at: string;
  orthography_profile: string;
  phonology_profile: string;
  gate_status: Record<string, GateStatus>;
  counts: Counts;
  sources: Record<string, SourceDto>;
  lemmas: LemmaDto[];
}