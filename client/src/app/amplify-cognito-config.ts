"use client";

import { Amplify } from "aws-amplify";
import { authConfig } from "./auth-config-export";

Amplify.configure(
  {
    Auth: authConfig,
  },
  { ssr: true } // server-side rendering to allow for amplify to use cookies for state storage
);

export default function ConfigureAmplifyClientSide() {
  return null;
}
