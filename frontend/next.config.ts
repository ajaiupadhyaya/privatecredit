import path from "path";
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Avoid inferring a parent folder as the workspace root when multiple lockfiles exist.
  turbopack: {
    root: path.join(__dirname),
  },
};

export default nextConfig;
