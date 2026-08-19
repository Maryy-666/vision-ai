export type AgentResponse = {
  status: "success" | "needs_information";
  session_id?: string;

  structured_request?: Record<string, any>;

  missing_information?: Array<{
    field: string;
    question: string;
    reason?: string;
  }>;

  analysis?: any;
};

export type ImageResponse = {
  status: string;

  filename: string;

  content_type: string;

  image: {
    width: number;
    height: number;
    mode: string;
    format: string;
  };

  vision_analysis?: {
    grayscale?: boolean;
    mean_intensity?: number;
    standard_deviation?: number;

    scratch_candidate_detection?: {
      method?: string;
      candidate_pixels?: number;
      candidate_ratio?: number;

      connected_components?: {
        candidate_count?: number;

        candidates?: Array<{
          label: number;
          x: number;
          y: number;
          width: number;
          height: number;
          area_pixels: number;

          centroid?: {
            x: number;
            y: number;
          };
        }>;
      };
    };
  };

  message?: string;
};

const API_URL = (
  process.env.EXPO_PUBLIC_API_URL ||
  "http://10.0.2.2:8000"
).replace(/\/$/, "");

async function parseResponse(response: Response) {
  const raw = await response.text();

  let data: any = {};

  try {
    data = raw ? JSON.parse(raw) : {};
  } catch {
    data = {
      detail: raw,
    };
  }

  if (!response.ok) {
    throw new Error(
      data?.detail ||
      `Request failed (${response.status})`
    );
  }

  return data;
}

export async function sendAgentMessage(
  message: string,
  sessionId?: string | null
): Promise<AgentResponse> {
  const response = await fetch(
    `${API_URL}/agent`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        message,
        session_id: sessionId ?? null,
      }),
    }
  );

  return parseResponse(response);
}

export async function uploadInspectionImage(
  uri: string,
  fileName = "inspection.jpg"
): Promise<ImageResponse> {
  const formData = new FormData();

  formData.append(
    "file",
    {
      uri,
      name: fileName,
      type: "image/jpeg",
    } as any
  );

  const response = await fetch(
    `${API_URL}/agent/image`,
    {
      method: "POST",
      body: formData,
    }
  );

  return parseResponse(response);
}

export function getApiUrl() {
  return API_URL;
}