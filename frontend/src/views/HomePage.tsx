import { Component } from 'react'
import Promo from "../components/PromoCard"
import ReadyCard from "../components/ReadyDive"


class Home extends Component {
    render() {
        return (
            <div>
                <Promo/>
                <ReadyCard/>
            </div>
        )
    }
}

export default Home
