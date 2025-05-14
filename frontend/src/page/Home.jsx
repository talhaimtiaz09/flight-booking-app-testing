import React from "react";
import { motion } from "framer-motion";
import HeroSection from "../components/Home/HeroSection";
import TopPlaces from "../components/Home/TopPlaces";
import ValuesWeProvide from "../components/Home/ValuesWeProvide";
import Testimonials from "../components/Home/Testimonials";
import LetGetToKnow from "../components/Home/LetGetToKnow";
import HomeTicketBookingBox from "../components/HomeTicketBookingBox";

const fadeInUp = {
  hidden: { opacity: 0, y: 30 },
  visible: (i = 0) => ({
    opacity: 1,
    y: 0,
    transition: {
      delay: i * 0.2,
      duration: 0.6,
      ease: "easeOut",
    },
  }),
};

const Home = () => {
  return (
    <section className="px-[30px] md:px-[30px]">
      {/* <motion.div
        custom={0}
        initial="hidden"
        animate="visible"
        variants={fadeInUp}
      >
        <HeroSection />
      </motion.div> */}

      <motion.div
        custom={1}
        initial="hidden"
        animate="visible"
        variants={fadeInUp}
      >
        <ValuesWeProvide />
      </motion.div>

      <motion.div
        custom={2}
        initial="hidden"
        animate="visible"
        variants={fadeInUp}
      >
        <HomeTicketBookingBox />
      </motion.div>

      <motion.div
        custom={3}
        initial="hidden"
        animate="visible"
        variants={fadeInUp}
      >
        <TopPlaces />
      </motion.div>

      <motion.div
        custom={4}
        initial="hidden"
        animate="visible"
        variants={fadeInUp}
      >
        <Testimonials />
      </motion.div>

      <motion.div
        custom={5}
        initial="hidden"
        animate="visible"
        variants={fadeInUp}
      >
        <LetGetToKnow />
      </motion.div>
    </section>
  );
};

export default Home;
