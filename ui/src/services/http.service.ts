import { api } from "./api";
import { AxiosResponse } from "axios";

interface SearchResponse {
  canthey: boolean;
}

export const searchUser = (name: string): Promise<AxiosResponse<SearchResponse>> => {
  return api.post("/search", { name });
};

export default {
  searchUser
};
