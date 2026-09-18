const path = require("path");
const express = require("express");
const cors = require("cors");
const config = require("./config");
const { requireAuth, loadUser } = require("./middleware/auth");
const { ensureCategories } = require("./services/seed");

const authRoutes = require("./routes/auth");
const expenseRoutes = require("./routes/expenses");
const budgetRoutes = require("./routes/budget");
const subscriptionRoutes = require("./routes/subscriptions");
const agentRoutes = require("./routes/agent");
const goalRoutes = require("./routes/goals");
const investmentRoutes = require("./routes/investments");
const alertRoutes = require("./routes/alerts");
const seedRoutes = require("./routes/seed");
const categoryRoutes = require("./routes/categories");
const profileRoutes = require("./routes/profile");

const app = express();
app.use(cors({ origin: true, credentials: true }));
app.use(express.json());

app.get("/health", (_req, res) => {
  res.json({ ok: true, service: "finance-guardian", env: config.nodeEnv });
});

if (config.nodeEnv !== "production") {
  app.get("/dev/profile-test", (_req, res) => {
    res.sendFile(path.join(__dirname, "..", "public", "dev-profile-test.html"));
  });
}

app.use("/api/auth", authRoutes);
app.use("/api/seed", seedRoutes);

const authed = [requireAuth, loadUser];
app.use("/api/profile", authed, profileRoutes);
app.use("/api/categories", authed, categoryRoutes);
app.use("/api/expenses", authed, expenseRoutes);
app.use("/api/budget", authed, budgetRoutes);
app.use("/api/budgets", authed, budgetRoutes);
app.use("/api/subscriptions", authed, subscriptionRoutes);
app.use("/api/agent", authed, agentRoutes);
app.use("/api/goals", authed, goalRoutes);
app.use("/api/investments", authed, investmentRoutes);
app.use("/api/alerts", authed, alertRoutes);

app.use((err, _req, res, _next) => {
  const status = err.status || 500;
  if (status >= 500) console.error(err);
  res.status(status).json({ error: err.message || "Internal server error" });
});

async function start() {
  await ensureCategories();
  app.listen(config.port, () => {
    console.log(`Finance Guardian API on http://localhost:${config.port}`);
  });
}

if (require.main === module) {
  start().catch((err) => {
    console.error(err);
    process.exit(1);
  });
}

module.exports = { app, start };
