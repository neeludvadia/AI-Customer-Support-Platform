import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// ─── Route Protection Middleware ─────────────────────────────────────────────
// Protects /dashboard and all sub-routes.
// Redirects to /login if no valid token is found.
// Redirects from /login to /dashboard if a valid token is found.

const PROTECTED_PREFIXES = ["/dashboard"];
const AUTH_PATHS = ["/login", "/register"];

const PUBLIC_PATHS = [
  "/api",
  "/_next",
  "/favicon.ico",
  "/manifest.json",
];

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // ── Allow public routes ──────────────────────────────────────────────────
  if (PUBLIC_PATHS.some((path) => pathname.startsWith(path))) {
    return NextResponse.next();
  }

  // ── Check token presence ─────────────────────────────────────────────────
  // We check for either access_token or refresh_token. 
  // If access_token is expired but refresh_token exists, the client-side fetchWithAuth
  // will handle the rotation transparently.
  const hasAccessToken = request.cookies.has("access_token");
  const hasRefreshToken = request.cookies.has("refresh_token");
  const hasAuth = hasAccessToken || hasRefreshToken;

  // ── Handle Auth Routes (/login, /register) ───────────────────────────────
  const isAuthRoute = AUTH_PATHS.some((path) => pathname.startsWith(path));
  if (isAuthRoute) {
    if (hasAuth) {
      // If user is already logged in, don't let them see the login page
      return NextResponse.redirect(new URL("/dashboard", request.url));
    }
    return NextResponse.next();
  }

  // ── Handle Protected Routes ──────────────────────────────────────────────
  const isProtected = PROTECTED_PREFIXES.some((prefix) =>
    pathname.startsWith(prefix)
  );

  if (isProtected) {
    if (!hasAuth) {
      // No tokens found, redirect to login
      return NextResponse.redirect(new URL("/login", request.url));
    }
    
    // Tokens exist, proceed to the protected route.
    // Deep validation will occur in the client-side data fetching.
    return NextResponse.next();
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (browser icon)
     */
    "/((?!_next/static|_next/image|favicon.ico).*)",
  ],
};
