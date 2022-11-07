import axios from "axios";

const apiUrl = "http://127.0.0.1:5000/api/v1";

export const postSignUp = async (form) => {
	try {
		const response = await axios.post(apiUrl + "/signUp", form);
		return response;
	} catch {}
};
