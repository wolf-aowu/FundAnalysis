const baseURL = "http://localhost:8000";
const developmentBaseURL = "http://localhost:8000";
const testingBaseURL = "http://localhost:8000";
const productionBaseURL = "http://localhost:8000";

export const BASE_URL =
    process.env.NODE_ENV === "development"
        ? developmentBaseURL
        : process.env.NODE_ENV === "testing"
        ? testingBaseURL
        : process.env.NODE_ENV === "production"
        ? productionBaseURL
        : baseURL;
export const TIMEOUT = 5000;
