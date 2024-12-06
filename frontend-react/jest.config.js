module.exports = {
    transform: {
      "^.+\\.(js|jsx|ts|tsx)$": "babel-jest",
    },
    testEnvironment: 'jest-environment-jsdom',
    setupFilesAfterEnv: ['@testing-library/jest-dom'],
    moduleNameMapper: {
      "\\.css$": "identity-obj-proxy", // For handling CSS imports
    },
    collectCoverageFrom: [
      "src/**/*.{js,jsx,ts,tsx}",
      "!src/**/*.d.ts", // Exclude type declarations from coverage
    ],
    coverageDirectory: "coverage",
    testMatch: ["**/src/**/*.test.{js,jsx,ts,tsx}"],
    moduleNameMapper: {
      '\\.css$': 'identity-obj-proxy', // This line tells Jest to mock CSS files
    },
  };
  