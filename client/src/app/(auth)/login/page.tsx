"use client";

import { CircleAlert, MoveRight } from "lucide-react";

import { useFormStatus } from "react-dom";
import { useActionState } from "react";
import { handleSignIn } from "@/lib/cognitoActions";
import Link from "next/link";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default function Login() {
  const [errorMessage, dispatch] = useActionState(handleSignIn, undefined);
  return (
    <form action={dispatch} className="space-y-3">
      <div className="flex-1 rounded-lg bg-gray-50 px-6 pb-4 pt-8">
        <h1 className={`mb-3 text-2xl`}>Login</h1>
        <div className="w-full">
          <div>
            <Label htmlFor="email">Email</Label>
            <Input
              className=""
              type="email"
              id="email"
              name="email"
              placeholder="Email Address"
              required
            />
          </div>
          <div>
            <Label htmlFor="password">Password</Label>
            <Input
              className=""
              id="password"
              name="password"
              type="password"
              placeholder="Enter password"
              required
              minLength={6}
            />
          </div>
        </div>
        <LoginButton />
        <div className="flex justify-center">
          <Link href="/signup" className="mt-2 cursor-pointer text-blue-500">
            {"Don't have an account? "} Sign up.
          </Link>
        </div>
        <div className="flex h-8 items-end space-x-1">
          <div
            className="flex h-8 items-end space-x-1"
            aria-live="polite"
            aria-atomic="true"
          >
            {errorMessage && (
              <>
                <CircleAlert className="h-5 w-5 text-red-500" />
                <p className="text-sm text-red-500">{errorMessage}</p>
              </>
            )}
          </div>
        </div>
      </div>
    </form>
  );
}

function LoginButton() {
  const { pending } = useFormStatus();

  return (
    <button className="mt-4 w-full" aria-disabled={pending}>
      Log in <MoveRight className="ml-auto h-5 w-5 text-gray-50" />
    </button>
  );
}
