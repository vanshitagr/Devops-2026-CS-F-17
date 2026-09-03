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