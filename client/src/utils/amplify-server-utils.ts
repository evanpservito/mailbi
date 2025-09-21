import { authConfig } from "@/app/auth-config-export";
import { NextServer, createServerRunner } from "@aws-amplify/adapter-nextjs";
import { fetchAuthSession, getCurrentUser } from "aws-amplify/auth/server";

export const { runWithAmplifyServerContext } = createServerRunner({
  config: {
    Auth: authConfig,
  },
});

export async function authenticatedUser(context: NextServer.Context) {
  return await runWithAmplifyServerContext({
    nextServerContext: context,
    operation: async (contextSpec) => {
      try {
        const session = await fetchAuthSession(contextSpec);
        if (!session.tokens) {
          return;
        }
        const user = {
          ...(await getCurrentUser(contextSpec)),
          isAdmin: false,
        };
        const groups = session.tokens.accessToken.payload["cognito:groups"];
        // @ts-expect-error: does not exist on type. ignore for now
        user.isAdmin = Boolean(groups && groups.includes("Admins"));
        return user;
      } catch (error) {
        console.log(error);
      }
    },
  });
}
