import { type NextRequest, NextResponse } from "next/server";
import { authenticatedUser } from "./utils/amplify-server-utils";

export async function middleware(request: NextRequest) {
  const response = NextResponse.next();
  const user = await authenticatedUser({ request, response });

  // TODO: make this logic cleaner
  const isOnDashboard =
    request.nextUrl.pathname.startsWith("/") &&
    !["/signup", "/confirm-signup", "/login"].includes(
      request.nextUrl.pathname
    );
  const isOnAdminArea = request.nextUrl.pathname.startsWith("/admins");

  if (isOnDashboard) {
    if (!user) return NextResponse.redirect(new URL("/login", request.nextUrl));
    if (isOnAdminArea && !user.isAdmin)
      return NextResponse.redirect(new URL("/overview", request.nextUrl));
    return response;
  } else if (user) {
    return NextResponse.redirect(new URL("/overview", request.nextUrl));
  }
}

export const config = {
  // Match all request paths except for ones starting with:
  matcher: ["/((?!api|_next/static|_next/image|.*\\.png$).*)"],
};
