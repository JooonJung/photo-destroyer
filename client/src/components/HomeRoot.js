import { VStack, HStack, Box, Text, Heading } from "@chakra-ui/layout";
import { Image } from "@chakra-ui/react";
import { useState } from "react";
import { Outlet } from "react-router";

const HomeRoot = () => {
	return (
		<HStack>
			<VStack
				bg={"#BCCEF8"}
				minW={"65vw"}
				minH={"100vh"}
				justifyContent={"center"}
				alignItems={"flex-end"}
			>
				<VStack
					border={"1px solid white"}
					borderRight={"none"}
					padding={50}
					color={"white"}
					minW={"85%"}
					maxH={"80vh"}
				>
					<Box position={"relative"} w={450} height={400} mx={"50px"}>
						<Image
							boxSize={"250"}
							position={"absolute"}
							left={0}
							bottom={10}
							src="https://bit.ly/dan-abramov"
							alt="Dan Abramov"
						/>
						<Image
							boxSize={"250"}
							position={"absolute"}
							right={0}
							top={10}
							src="https://bit.ly/dan-abramov"
							alt="Dan Abramov"
						/>
					</Box>
					<Heading
						textAlign={"center"}
						maxW={"350"}
						fontSize={"3xl"}
						lineHeight={"8"}
					>
						Lorem ipsum dolor sit amet, consectetur adipiscing elit.
					</Heading>
					<Text textAlign={"center"}>
						Lorem ipsum dolor sit amet, consectetur.
						<br />
						Lorem ipsum consectetur.
					</Text>
				</VStack>
			</VStack>
			<Box minW={"35vw"}>
				<Outlet />
			</Box>
		</HStack>
	);
};

export default HomeRoot;
