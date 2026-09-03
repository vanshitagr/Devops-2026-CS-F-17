// Centralized error handler. Routes can call next(err) instead of
// writing their own res.status(500).json({...}) in every catch block.
export const errorHandler = (err, req, res, next) => {
  console.error(err.stack);
  const statusCode = res.statusCode === 200 ? 500 : res.statusCode;
  res.status(statusCode).json({
    message: err.message || "Something went wrong on the server",
  });
};