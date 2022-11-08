import axios from "axios";

const instance = axios.create({
	baseURL: "http://127.0.0.1:5000/api/v1/",
});

export const postSignUp = async (form) => {
	const response = await instance.post(`/signUp`, form);
	return response;
};

export const postLogin = async (form) => {
	const response = await instance.post(`/login`, form);
	return response;
};
