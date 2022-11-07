import { useForm } from "react-hook-form";
import {
	FormControl,
	FormLabel,
	FormErrorMessage,
	FormHelperText,
} from "@chakra-ui/react";
import { Input } from "@chakra-ui/input";
import { Button } from "@chakra-ui/button";
import { Heading, Text, VStack } from "@chakra-ui/layout";
import { Form, Link as RouterLink } from "react-router-dom";

const SignUp = () => {
	const { register, handleSubmit } = useForm();
	const onSubmit = (data) => console.log(data);

	return (
		<VStack>
			<VStack alignItems={"flex-start"} w={400}>
				<Heading>회원가입</Heading>
				<Text>Lorem ipsum dolor sit amet, consectetur.</Text>
				<VStack as={"form"} onSubmit={handleSubmit(onSubmit)} w={"100%"}>
					<FormControl w={"100%"}>
						<FormLabel>별명</FormLabel>
						<Input placeholder={"ex) 포토덕후"} />
					</FormControl>
					<FormControl w={"100%"}>
						<FormLabel>이메일</FormLabel>
						<Input placeholder={"example@mail.com"} type="email" />
					</FormControl>
					<FormControl w={"100%"}>
						<FormLabel>비밀번호</FormLabel>
						<Input
							type="password"
							placeholder={"8자 이상의 영대소문자와 특수기호를 포함한 비밀번호"}
						/>
					</FormControl>
					<FormControl w={"100%"} pb={30}>
						<FormLabel>비밀번호 확인</FormLabel>
						<Input type="password" placeholder={"비밀번호 확인"} />
					</FormControl>
					<Button type={"submit"} w={"100%"} bg={"#BCCEF8"} color={"white"}>
						회원가입
					</Button>
				</VStack>
				<Text>
					이미 계정이 있으신가요?
					<Button color={"blue.300"} variant={"link"}>
						<RouterLink to={"/login"}>로그인</RouterLink>
					</Button>
				</Text>
			</VStack>
		</VStack>
	);
};

export default SignUp;
