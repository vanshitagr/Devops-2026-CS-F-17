const requiredEnvironment = ["MONGO_URI", "JWT_SECRET"];

export const validateEnvironment = () => {
  if (process.env.NODE_ENV === "test") return;
  const missing = requiredEnvironment.filter(
    (key) => !process.env[key]
  );

  if (missing.length > 0) {
    console.warn(
      `[WARN] Missing environment variables: ${missing.join(", ")}. Using fallback/local defaults.`
    );
  }
};

export default validateEnvironment;
