import { Sun, Moon } from "react-feather"
import useDarkMode from "../custom_hooks/useDarkMode"


export default function ThemeToggle() {
    const [colorTheme, setTheme] = useDarkMode()
    return (
        <div>
            <span onClick={() => setTheme(colorTheme)}>
                {colorTheme === "light" ?
                    <Sun />
                    :
                    <Moon />
                }
            </span>
        </div>
    )
}
