#------------------------------------------
# Imports are the very first thing you'll do in any project
# Imports allow you to work with certain subsets/data/analysis work
#------------------------------------------
import seaborn as sns
from faicons import icon_svg

from shiny import reactive
from shiny.express import input, render, ui
import palmerpenguins
import shinyswatch
df = palmerpenguins.load_penguins()
#------------------------------------------
#Theme of Project
#------------------------------------------
shinyswatch.theme.slate()

#------------------------------------------
#Page Options are the Title of your project
#------------------------------------------

ui.page_opts(title="🐧 Nollette Penguin Dataset: Exploring The Species", fillable=True)

#------------------------------------------
#Define the Sidebar
#Sidebar isn't always necessary, but allows for user interaction
#------------------------------------------

with ui.sidebar(title="🔬 Penguin Characteristics"):
    ui.input_slider("mass", "⚖️ Mass", 2000, 6000, 6000)
    ui.input_checkbox_group(
        "species",
        "🧬 Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    ui.hr()
    ui.h6("📨 Links")
    ui.a(
        "GitHub Source",
        href="https://github.com/nollettecs/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://github.com/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/nollettecs/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )
#------------------------------------------
#Main section of your project
#You can add/subtract cards, value boxes, grids, charts, tables, etc.
#Get creative because this is the heart of your project
#------------------------------------------

with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("earlybirds"), theme="bg-gradient-blue-green"):
        "Number of penguins"

        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("ruler-horizontal"), theme="bg-gradient-blue-green"):
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box(showcase=icon_svg("ruler-vertical"), theme="bg-gradient-blue-green"):
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"


with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Bill length and depth")

        @render.plot
        def length_depth():
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
            )

    with ui.card(full_screen=True):
        ui.card_header("Penguin Data")

        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)

#------------------------------------------
#Define a reactive calc to filter the dataset
#------------------------------------------
#ui.include_css(app_dir / "styles.css")


@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
