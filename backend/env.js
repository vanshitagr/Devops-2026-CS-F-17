const requiredEnvironment = ["MONGO_URI", "JWT_SECRET"];

export const validateEnvironment = () => {
  const missing = requiredEnvironment.filter(
    (key) => !process.env[key]
  );

  if (missing.length > 0) {
    throw new Error(
      `Missing required environment variables: ${missing.join(", ")}`
    );
  }
};