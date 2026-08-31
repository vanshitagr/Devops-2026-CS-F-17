const requests = new Map();

const WINDOW_MS = 60 * 1000;
const MAX_REQUESTS = 100;

const rateLimiter = (req, res, next) => {
  const key = req.ip;
  const now = Date.now();

  const record = requests.get(key);

  if (!record || now - record.start > WINDOW_MS) {
    requests.set(key, {
      start: now,
      count: 1,
    });

    return next();
  }

  record.count += 1;

  if (record.count > MAX_REQUESTS) {
    return res.status(429).json({
      success: false,
      message: "Too many requests. Please try again later.",
    });
  }

  next();
};

export default rateLimiter;