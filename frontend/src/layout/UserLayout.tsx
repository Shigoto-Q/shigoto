import Footer from "../components/Footer"

const Layout = (props: any) => {
    return (
        <div className="container mx-auto">
            {props.children}
            <Footer />
        </div>
    )
}

export default Layout
