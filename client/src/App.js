import React, { useState, useEffect } from "react";
import axios from "axios";

import { apiRouter } from "./utils";

function App() {
	const [currentTime, setCurrentTime] = useState(0);
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState(null);

	useEffect(() => {
		const fetchTime = async () => {
			try {
				setLoading(true);
				setError(null);
				const response = await axios.get(apiRouter("/"));
				setCurrentTime(response.data.time);
			} catch (error) {
				setError(error);
			}
			setLoading(false);
		};

		fetchTime();
	}, []);

	if (loading) return <div>로딩중</div>;
	if (error) return <div>에러가 발생했습니다</div>;
	return (
		<div className="App">
			<header className="App-header">
				<p>The current time is {currentTime}.</p>
			</header>
		</div>
	);
}

export default App;
