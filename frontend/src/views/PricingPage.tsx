import { Component } from 'react'
import PricingCard from "../components/PricingCard"

type MyProps = {
  message: string;
};


class Pricing extends Component<MyProps> {
    render() {
        return (
        <div>
            <h1 className="font-mono text-center text-purple-700 text-2xl subpixel-antialiased font-semibold"> Select a plan: </h1>
                <div className="flex space-x-10 justify-center">
                    <PricingCard/>
                    <PricingCard/>
                    <PricingCard/>
                    <PricingCard/>
                    <PricingCard/>
                </div>
            </div>
        )
    }
}

export default Pricing
