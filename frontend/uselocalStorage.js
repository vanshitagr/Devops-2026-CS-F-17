import { useState } from "react";

// Syncs a piece of state with localStorage under the given key,
// so the value survives a page refresh.
export function useLocalStorage(key, initialValue) {
  const [value, setValue] = useState(() => {
    try {
      const stored = localStorage.getItem(key);
      return stored !== null ? JSON.parse(stored) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setStoredValue = (newValue) => {
    setValue(newValue);
    try {
      localStorage.setItem(key, JSON.stringify(newValue));
    } catch {
      // localStorage unavailable (private browsing, etc.) — fail silently
    }
  };

  return [value, setStoredValue];
}