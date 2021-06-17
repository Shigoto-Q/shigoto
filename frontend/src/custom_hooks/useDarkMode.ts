import { useEffect, useState } from 'react'

export default function useDarkMode() {
    const [theme, setTheme] = useState(localStorage.getItem("theme") || "light")
    const colorTheme = theme === 'light' ? 'dark' : 'light'

    useEffect(() => {
        const root = window.document.documentElement
        root.classList.remove(colorTheme)
        root.classList.add(theme)
        localStorage.setItem("theme", theme)
    }, [theme, colorTheme])
    return [colorTheme, setTheme] as const
}
