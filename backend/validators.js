export const isValidEmail = (email) => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
};

export const isValidPassword = (password) => {
  return typeof password === "string" && password.length >= 6;
};

export const isNonEmptyString = (value) => {
  return typeof value === "string" && value.trim().length > 0;
};

export const isPositiveNumber = (value) => {
  return Number.isFinite(Number(value)) && Number(value) > 0;
};
export const getPasswordValidationErrors = (password) => {
  const errors = [];

  if (typeof password !== "string") {
    return ["Password must be a string"];
  }

  if (password.length < 6) {
    errors.push("Password must be at least 6 characters long");
  }

  if (password.length > 128) {
    errors.push("Password must not exceed 128 characters");
  }

  return errors;
};