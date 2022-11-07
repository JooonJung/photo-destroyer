import { createBrowserRouter } from "react-router-dom";
import NotFound from "./routes/NotFound";
import HomeRoot from "./components/HomeRoot";
import Home from "./routes/Home/Home";
import Login from "./routes/Home/Login";
import SignUp from "./routes/Home/SignUp";

const router = createBrowserRouter([
	{
		path: "/",
		element: <HomeRoot />,
		errorElement: <NotFound />,
		children: [
			{
				path: "",
				element: <Home />,
			},
			{
				path: "login",
				element: <Login />,
			},
			{
				path: "signup",
				element: <SignUp />,
			},
		],
	},
]);

export default router;
