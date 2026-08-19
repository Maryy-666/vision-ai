import React, {
  createContext,
  useContext,
  useMemo,
  useState,
} from "react";

import type {
  AgentResponse,
  ImageResponse,
} from "../lib/api";

type InspectionContextValue = {
  sessionId: string | null;

  requirement: string;

  agentResponse: AgentResponse | null;

  imageUri: string | null;

  imageResponse: ImageResponse | null;

  setRequirement: (
    value: string
  ) => void;

  setAgentResponse: (
    value: AgentResponse | null
  ) => void;

  setSessionId: (
    value: string | null
  ) => void;

  setImageUri: (
    value: string | null
  ) => void;

  setImageResponse: (
    value: ImageResponse | null
  ) => void;

  reset: () => void;
};

const InspectionContext =
  createContext<InspectionContextValue | null>(
    null
  );

export function InspectionProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [
    sessionId,
    setSessionId,
  ] = useState<string | null>(null);

  const [
    requirement,
    setRequirement,
  ] = useState("");

  const [
    agentResponse,
    setAgentResponse,
  ] = useState<AgentResponse | null>(null);

  const [
    imageUri,
    setImageUri,
  ] = useState<string | null>(null);

  const [
    imageResponse,
    setImageResponse,
  ] = useState<ImageResponse | null>(
    null
  );

  const value = useMemo(
    () => ({
      sessionId,
      requirement,
      agentResponse,
      imageUri,
      imageResponse,

      setRequirement,
      setAgentResponse,
      setSessionId,
      setImageUri,
      setImageResponse,

      reset: () => {
        setSessionId(null);
        setRequirement("");
        setAgentResponse(null);
        setImageUri(null);
        setImageResponse(null);
      },
    }),
    [
      sessionId,
      requirement,
      agentResponse,
      imageUri,
      imageResponse,
    ]
  );

  return (
    <InspectionContext.Provider
      value={value}
    >
      {children}
    </InspectionContext.Provider>
  );
}

export function useInspection() {
  const context =
    useContext(InspectionContext);

  if (!context) {
    throw new Error(
      "useInspection must be used inside InspectionProvider"
    );
  }

  return context;
}