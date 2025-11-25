export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type Database = {
  // Allows to automatically instantiate createClient with right options
  // instead of createClient<Database, { PostgrestVersion: 'XX' }>(URL, KEY)
  __InternalSupabase: {
    PostgrestVersion: "13.0.5"
  }
  public: {
    Tables: {
      audit_log: {
        Row: {
          action: string
          changed_at: string | null
          changed_by: string | null
          id: string
          ip_address: unknown
          metadata: Json | null
          new_data: Json | null
          old_data: Json | null
          record_id: string
          table_name: string
          user_agent: string | null
        }
        Insert: {
          action: string
          changed_at?: string | null
          changed_by?: string | null
          id?: string
          ip_address?: unknown
          metadata?: Json | null
          new_data?: Json | null
          old_data?: Json | null
          record_id: string
          table_name: string
          user_agent?: string | null
        }
        Update: {
          action?: string
          changed_at?: string | null
          changed_by?: string | null
          id?: string
          ip_address?: unknown
          metadata?: Json | null
          new_data?: Json | null
          old_data?: Json | null
          record_id?: string
          table_name?: string
          user_agent?: string | null
        }
        Relationships: []
      }
      compliance_checks: {
        Row: {
          category: string | null
          checked_at: string | null
          created_at: string | null
          created_by: string | null
          deleted_at: string | null
          evidence: Json | null
          id: string
          issues: Json | null
          metadata: Json | null
          notes: string | null
          project_id: string
          recommendations: Json | null
          reviewer: string | null
          score: number | null
          standard: string
          status: Database["public"]["Enums"]["compliance_status"] | null
          updated_at: string | null
        }
        Insert: {
          category?: string | null
          checked_at?: string | null
          created_at?: string | null
          created_by?: string | null
          deleted_at?: string | null
          evidence?: Json | null
          id?: string
          issues?: Json | null
          metadata?: Json | null
          notes?: string | null
          project_id: string
          recommendations?: Json | null
          reviewer?: string | null
          score?: number | null
          standard: string
          status?: Database["public"]["Enums"]["compliance_status"] | null
          updated_at?: string | null
        }
        Update: {
          category?: string | null
          checked_at?: string | null
          created_at?: string | null
          created_by?: string | null
          deleted_at?: string | null
          evidence?: Json | null
          id?: string
          issues?: Json | null
          metadata?: Json | null
          notes?: string | null
          project_id?: string
          recommendations?: Json | null
          reviewer?: string | null
          score?: number | null
          standard?: string
          status?: Database["public"]["Enums"]["compliance_status"] | null
          updated_at?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "compliance_checks_project_id_fkey"
            columns: ["project_id"]
            isOneToOne: false
            referencedRelation: "projects"
            referencedColumns: ["id"]
          },
        ]
      }
      documents: {
        Row: {
          confidence_score: number | null
          created_at: string | null
          created_by: string | null
          deleted_at: string | null
          embeddings_id: string | null
          extracted_data: Json | null
          file_path: string | null
          file_size: number | null
          id: string
          language: string | null
          metadata: Json | null
          mime_type: string | null
          name: string
          page_count: number | null
          processed: boolean | null
          processed_at: string | null
          processing_status: string | null
          project_id: string
          type: Database["public"]["Enums"]["document_type"]
          updated_at: string | null
          url: string | null
        }
        Insert: {
          confidence_score?: number | null
          created_at?: string | null
          created_by?: string | null
          deleted_at?: string | null
          embeddings_id?: string | null
          extracted_data?: Json | null
          file_path?: string | null
          file_size?: number | null
          id?: string
          language?: string | null
          metadata?: Json | null
          mime_type?: string | null
          name: string
          page_count?: number | null
          processed?: boolean | null
          processed_at?: string | null
          processing_status?: string | null
          project_id: string
          type: Database["public"]["Enums"]["document_type"]
          updated_at?: string | null
          url?: string | null
        }
        Update: {
          confidence_score?: number | null
          created_at?: string | null
          created_by?: string | null
          deleted_at?: string | null
          embeddings_id?: string | null
          extracted_data?: Json | null
          file_path?: string | null
          file_size?: number | null
          id?: string
          language?: string | null
          metadata?: Json | null
          mime_type?: string | null
          name?: string
          page_count?: number | null
          processed?: boolean | null
          processed_at?: string | null
          processing_status?: string | null
          project_id?: string
          type?: Database["public"]["Enums"]["document_type"]
          updated_at?: string | null
          url?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "documents_project_id_fkey"
            columns: ["project_id"]
            isOneToOne: false
            referencedRelation: "projects"
            referencedColumns: ["id"]
          },
        ]
      }
      financial_models: {
        Row: {
          assumptions: Json
          created_at: string | null
          created_by: string | null
          currency: string | null
          dcf_analysis: Json | null
          deleted_at: string | null
          discount_rate: number | null
          id: string
          irr: number | null
          metadata: Json | null
          model_type: string
          npv: number | null
          outputs: Json | null
          payback_period: number | null
          project_id: string
          project_life_years: number | null
          risk_metrics: Json | null
          scenarios: Json | null
          sensitivity_analysis: Json | null
          updated_at: string | null
          version: number | null
        }
        Insert: {
          assumptions?: Json
          created_at?: string | null
          created_by?: string | null
          currency?: string | null
          dcf_analysis?: Json | null
          deleted_at?: string | null
          discount_rate?: number | null
          id?: string
          irr?: number | null
          metadata?: Json | null
          model_type: string
          npv?: number | null
          outputs?: Json | null
          payback_period?: number | null
          project_id: string
          project_life_years?: number | null
          risk_metrics?: Json | null
          scenarios?: Json | null
          sensitivity_analysis?: Json | null
          updated_at?: string | null
          version?: number | null
        }
        Update: {
          assumptions?: Json
          created_at?: string | null
          created_by?: string | null
          currency?: string | null
          dcf_analysis?: Json | null
          deleted_at?: string | null
          discount_rate?: number | null
          id?: string
          irr?: number | null
          metadata?: Json | null
          model_type?: string
          npv?: number | null
          outputs?: Json | null
          payback_period?: number | null
          project_id?: string
          project_life_years?: number | null
          risk_metrics?: Json | null
          scenarios?: Json | null
          sensitivity_analysis?: Json | null
          updated_at?: string | null
          version?: number | null
        }
        Relationships: [
          {
            foreignKeyName: "financial_models_project_id_fkey"
            columns: ["project_id"]
            isOneToOne: false
            referencedRelation: "projects"
            referencedColumns: ["id"]
          },
        ]
      }
      projects: {
        Row: {
          country: string
          created_at: string | null
          created_by: string | null
          currency: string | null
          deleted_at: string | null
          description: string | null
          dfi_partners: Json | null
          id: string
          location: Json | null
          metadata: Json | null
          name: string
          risk_score: number | null
          sector: Database["public"]["Enums"]["sector_type"]
          sponsor: string | null
          stakeholders: Json | null
          status: Database["public"]["Enums"]["project_status"] | null
          timeline: Json | null
          total_value: number | null
          updated_at: string | null
          updated_by: string | null
        }
        Insert: {
          country: string
          created_at?: string | null
          created_by?: string | null
          currency?: string | null
          deleted_at?: string | null
          description?: string | null
          dfi_partners?: Json | null
          id?: string
          location?: Json | null
          metadata?: Json | null
          name: string
          risk_score?: number | null
          sector: Database["public"]["Enums"]["sector_type"]
          sponsor?: string | null
          stakeholders?: Json | null
          status?: Database["public"]["Enums"]["project_status"] | null
          timeline?: Json | null
          total_value?: number | null
          updated_at?: string | null
          updated_by?: string | null
        }
        Update: {
          country?: string
          created_at?: string | null
          created_by?: string | null
          currency?: string | null
          deleted_at?: string | null
          description?: string | null
          dfi_partners?: Json | null
          id?: string
          location?: Json | null
          metadata?: Json | null
          name?: string
          risk_score?: number | null
          sector?: Database["public"]["Enums"]["sector_type"]
          sponsor?: string | null
          stakeholders?: Json | null
          status?: Database["public"]["Enums"]["project_status"] | null
          timeline?: Json | null
          total_value?: number | null
          updated_at?: string | null
          updated_by?: string | null
        }
        Relationships: []
      }
      reports: {
        Row: {
          content: Json
          created_at: string | null
          created_by: string | null
          deleted_at: string | null
          file_url: string | null
          format: string | null
          generated_by: string | null
          id: string
          metadata: Json | null
          project_id: string
          report_type: string
          template_used: string | null
          title: string
          updated_at: string | null
        }
        Insert: {
          content: Json
          created_at?: string | null
          created_by?: string | null
          deleted_at?: string | null
          file_url?: string | null
          format?: string | null
          generated_by?: string | null
          id?: string
          metadata?: Json | null
          project_id: string
          report_type: string
          template_used?: string | null
          title: string
          updated_at?: string | null
        }
        Update: {
          content?: Json
          created_at?: string | null
          created_by?: string | null
          deleted_at?: string | null
          file_url?: string | null
          format?: string | null
          generated_by?: string | null
          id?: string
          metadata?: Json | null
          project_id?: string
          report_type?: string
          template_used?: string | null
          title?: string
          updated_at?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "reports_project_id_fkey"
            columns: ["project_id"]
            isOneToOne: false
            referencedRelation: "projects"
            referencedColumns: ["id"]
          },
        ]
      }
      risk_assessments: {
        Row: {
          assessed_by: string | null
          assessment_date: string | null
          assessment_type: string
          country_risk: Json | null
          created_at: string | null
          created_by: string | null
          deleted_at: string | null
          environmental_risk: Json | null
          financial_risk: Json | null
          id: string
          identified_risks: Json | null
          metadata: Json | null
          mitigation_strategies: Json | null
          overall_risk_score: number | null
          political_risk: Json | null
          project_id: string
          risk_categories: Json | null
          risk_matrix: Json | null
          technical_risk: Json | null
          updated_at: string | null
        }
        Insert: {
          assessed_by?: string | null
          assessment_date?: string | null
          assessment_type: string
          country_risk?: Json | null
          created_at?: string | null
          created_by?: string | null
          deleted_at?: string | null
          environmental_risk?: Json | null
          financial_risk?: Json | null
          id?: string
          identified_risks?: Json | null
          metadata?: Json | null
          mitigation_strategies?: Json | null
          overall_risk_score?: number | null
          political_risk?: Json | null
          project_id: string
          risk_categories?: Json | null
          risk_matrix?: Json | null
          technical_risk?: Json | null
          updated_at?: string | null
        }
        Update: {
          assessed_by?: string | null
          assessment_date?: string | null
          assessment_type?: string
          country_risk?: Json | null
          created_at?: string | null
          created_by?: string | null
          deleted_at?: string | null
          environmental_risk?: Json | null
          financial_risk?: Json | null
          id?: string
          identified_risks?: Json | null
          metadata?: Json | null
          mitigation_strategies?: Json | null
          overall_risk_score?: number | null
          political_risk?: Json | null
          project_id?: string
          risk_categories?: Json | null
          risk_matrix?: Json | null
          technical_risk?: Json | null
          updated_at?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "risk_assessments_project_id_fkey"
            columns: ["project_id"]
            isOneToOne: false
            referencedRelation: "projects"
            referencedColumns: ["id"]
          },
        ]
      }
      stakeholders: {
        Row: {
          contact_email: string | null
          contact_phone: string | null
          country: string | null
          created_at: string | null
          created_by: string | null
          deleted_at: string | null
          engagement_status: string | null
          id: string
          influence_level: string | null
          metadata: Json | null
          name: string
          notes: string | null
          organization: string | null
          project_id: string
          role: string
          stakeholder_type: string | null
          updated_at: string | null
        }
        Insert: {
          contact_email?: string | null
          contact_phone?: string | null
          country?: string | null
          created_at?: string | null
          created_by?: string | null
          deleted_at?: string | null
          engagement_status?: string | null
          id?: string
          influence_level?: string | null
          metadata?: Json | null
          name: string
          notes?: string | null
          organization?: string | null
          project_id: string
          role: string
          stakeholder_type?: string | null
          updated_at?: string | null
        }
        Update: {
          contact_email?: string | null
          contact_phone?: string | null
          country?: string | null
          created_at?: string | null
          created_by?: string | null
          deleted_at?: string | null
          engagement_status?: string | null
          id?: string
          influence_level?: string | null
          metadata?: Json | null
          name?: string
          notes?: string | null
          organization?: string | null
          project_id?: string
          role?: string
          stakeholder_type?: string | null
          updated_at?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "stakeholders_project_id_fkey"
            columns: ["project_id"]
            isOneToOne: false
            referencedRelation: "projects"
            referencedColumns: ["id"]
          },
        ]
      }
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      can_create_initial_owner: {
        Args: { team_uuid: string }
        Returns: boolean
      }
      is_team_member: { Args: { team_uuid: string }; Returns: boolean }
      is_team_owner: { Args: { team_uuid: string }; Returns: boolean }
      show_limit: { Args: never; Returns: number }
      show_trgm: { Args: { "": string }; Returns: string[] }
    }
    Enums: {
      CollaboratorRole: "OWNER" | "EDITOR" | "COMMENTER" | "VIEWER"
      compliance_status:
        | "pending"
        | "in_progress"
        | "compliant"
        | "non_compliant"
        | "needs_review"
        | "approved"
      context_type:
        | "market_analysis"
        | "technical_specs"
        | "team_roles"
        | "project_goals"
        | "user_personas"
        | "business_rules"
      document_type:
        | "feasibility_study"
        | "financial_model"
        | "environmental_impact"
        | "technical_specification"
        | "legal_agreement"
        | "compliance_report"
        | "investment_memo"
        | "due_diligence"
        | "other"
      ExportFormat: "PDF" | "PPTX" | "PNG" | "VIDEO" | "HTML"
      JobStatus: "PENDING" | "PROCESSING" | "COMPLETED" | "FAILED" | "CANCELLED"
      project_status:
        | "draft"
        | "pipeline"
        | "under_review"
        | "approved"
        | "rejected"
        | "active"
        | "completed"
        | "cancelled"
      prompt_category:
        | "ai_features"
        | "backend"
        | "frontend"
        | "marketing"
        | "research"
        | "general"
      Role: "USER" | "ADMIN" | "MODERATOR"
      sector_type:
        | "renewable_energy"
        | "green_hydrogen"
        | "transmission"
        | "water"
        | "transportation"
        | "waste_management"
        | "other"
      team_role: "owner" | "admin" | "member" | "viewer"
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

type DatabaseWithoutInternals = Omit<Database, "__InternalSupabase">

type DefaultSchema = DatabaseWithoutInternals[Extract<keyof Database, "public">]

export type Tables<
  DefaultSchemaTableNameOrOptions extends
    | keyof (DefaultSchema["Tables"] & DefaultSchema["Views"])
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
        DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
      DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])[TableName] extends {
      Row: infer R
    }
    ? R
    : never
  : DefaultSchemaTableNameOrOptions extends keyof (DefaultSchema["Tables"] &
        DefaultSchema["Views"])
    ? (DefaultSchema["Tables"] &
        DefaultSchema["Views"])[DefaultSchemaTableNameOrOptions] extends {
        Row: infer R
      }
      ? R
      : never
    : never

export type TablesInsert<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Insert: infer I
    }
    ? I
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Insert: infer I
      }
      ? I
      : never
    : never

export type TablesUpdate<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Update: infer U
    }
    ? U
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Update: infer U
      }
      ? U
      : never
    : never

export type Enums<
  DefaultSchemaEnumNameOrOptions extends
    | keyof DefaultSchema["Enums"]
    | { schema: keyof DatabaseWithoutInternals },
  EnumName extends DefaultSchemaEnumNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"]
    : never = never,
> = DefaultSchemaEnumNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"][EnumName]
  : DefaultSchemaEnumNameOrOptions extends keyof DefaultSchema["Enums"]
    ? DefaultSchema["Enums"][DefaultSchemaEnumNameOrOptions]
    : never

export type CompositeTypes<
  PublicCompositeTypeNameOrOptions extends
    | keyof DefaultSchema["CompositeTypes"]
    | { schema: keyof DatabaseWithoutInternals },
  CompositeTypeName extends PublicCompositeTypeNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"]
    : never = never,
> = PublicCompositeTypeNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"][CompositeTypeName]
  : PublicCompositeTypeNameOrOptions extends keyof DefaultSchema["CompositeTypes"]
    ? DefaultSchema["CompositeTypes"][PublicCompositeTypeNameOrOptions]
    : never

export const Constants = {
  public: {
    Enums: {
      CollaboratorRole: ["OWNER", "EDITOR", "COMMENTER", "VIEWER"],
      compliance_status: [
        "pending",
        "in_progress",
        "compliant",
        "non_compliant",
        "needs_review",
        "approved",
      ],
      context_type: [
        "market_analysis",
        "technical_specs",
        "team_roles",
        "project_goals",
        "user_personas",
        "business_rules",
      ],
      document_type: [
        "feasibility_study",
        "financial_model",
        "environmental_impact",
        "technical_specification",
        "legal_agreement",
        "compliance_report",
        "investment_memo",
        "due_diligence",
        "other",
      ],
      ExportFormat: ["PDF", "PPTX", "PNG", "VIDEO", "HTML"],
      JobStatus: ["PENDING", "PROCESSING", "COMPLETED", "FAILED", "CANCELLED"],
      project_status: [
        "draft",
        "pipeline",
        "under_review",
        "approved",
        "rejected",
        "active",
        "completed",
        "cancelled",
      ],
      prompt_category: [
        "ai_features",
        "backend",
        "frontend",
        "marketing",
        "research",
        "general",
      ],
      Role: ["USER", "ADMIN", "MODERATOR"],
      sector_type: [
        "renewable_energy",
        "green_hydrogen",
        "transmission",
        "water",
        "transportation",
        "waste_management",
        "other",
      ],
      team_role: ["owner", "admin", "member", "viewer"],
    },
  },
} as const
