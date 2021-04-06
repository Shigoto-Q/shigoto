import Navbar from "../components/Navbar"
import Footer from "../components/Footer"

const Layout = (props: any) => {
    return (
        <div className="container mx-auto">
            <Navbar />
            {props.children}
            <Footer />
        </div>
    )
}

export default Layout
