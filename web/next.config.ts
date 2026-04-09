import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",
  trailingSlash: true,
  basePath: "/procurement-wiki",
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
