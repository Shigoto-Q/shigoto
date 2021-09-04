import Navbar from "../components/Navbar"
import Footer from "../components/Footer"
import Particles from "react-tsparticles";


const Layout = (props: any) => {
    return (
        <div className="flex flex-col h-screen">
            <header className="text-gray-600 body-font">
                <Navbar />
            </header>
            <div className="flex-grow">
                {props.children}
            </div>
            <Footer />
        </div>
    )
}

export default Layout
