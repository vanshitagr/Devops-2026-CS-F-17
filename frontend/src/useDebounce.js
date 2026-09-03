import { useState, useEffect } from "react";

// Delays updating the returned value until the user has stopped
// typing for `delay` ms — prevents firing an API call on every
// keystroke when used with a search input.
export function useDebounce(value, delay = 400) {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debounced;
}