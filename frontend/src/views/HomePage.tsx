import { Component } from 'react'
import Promo from "../components/PromoCard"
import ReadyCard from "../components/ReadyDive"
import pageTransition from "../layout/transitions"
import { motion } from "framer-motion"

const homeTransition = {
    type: "tween",
    ease: "anticipate",
    duration: 0.8
}
class Home extends Component {
    constructor(props: any) {
        super(props);
    }

    render() {
        return (
            <div>
                <motion.div initial="out" animate="in" exit="out" variants={pageTransition} transition={homeTransition}>
                    <Promo />
                    <ReadyCard />
                </motion.div>
            </div>
        )
    }
}

export default Home
