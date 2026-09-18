const path = require("path");
require("dotenv").config({ path: path.join(__dirname, "..", ".env") });

module.exports = {
  port: Number(process.env.PORT || 4000),
  nodeEnv: process.env.NODE_ENV || "development",
  jwtSecret: process.env.JWT_SECRET || "dev-insecure-secret",
  jwtExpiresIn: process.env.JWT_EXPIRES_IN || "7d",
  openaiApiKey: process.env.OPENAI_API_KEY || "",
  openaiModel: process.env.OPENAI_MODEL || "gpt-4o-mini",
  anthropicApiKey: process.env.ANTHROPIC_API_KEY || "",
  anthropicModel: process.env.ANTHROPIC_MODEL || "claude-3-5-haiku-20241022",
  alphaVantageApiKey: process.env.ALPHA_VANTAGE_API_KEY || "",
};
