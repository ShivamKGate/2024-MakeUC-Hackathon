# fact.py

# List of environmental facts
environmental_facts = [
    "Recycling one aluminum can save enough energy to run a TV for three hours.",
    "The average person generates over 4 pounds of trash every day and about 1.5 tons of solid waste per year.",
    "Only about 25% of the plastic produced in the U.S. is recycled.",
    "Approximately 1 million sea birds and 100,000 sea mammals are killed by pollution every year.",
    "Recycling plastic saves twice as much energy as burning it in an incinerator.",
    "The average American uses 500 plastic bags per year, only 1% of which are returned for recycling.",
    "The Great Pacific Garbage Patch is a collection of marine debris in the North Pacific Ocean, about twice the size of Texas.",
    "By 2050, it is estimated that there will be more plastic in the oceans than fish by weight.",
    "Recycling one ton of paper saves 17 trees, 7,000 gallons of water, and 3 cubic yards of landfill space.",
    "Deforestation is responsible for about 10-15% of global greenhouse gas emissions.",
    "About 27,000 trees are cut down every day to produce toilet paper.",
    "The Earth’s ozone layer, which blocks harmful UV rays, has been recovering since the 1987 Montreal Protocol.",
    "Air pollution is estimated to cause 4.2 million deaths globally each year.",
    "Around 8 million tons of plastic waste enter the oceans every year.",
    "Coral reefs provide a home for 25% of all marine life, despite covering less than 1% of the ocean floor.",
    "It takes about 500 years for plastic to degrade in a landfill.",
    "Every ton of recycled paper saves about 380 gallons of oil.",
    "An estimated 18 million acres of forest are lost each year, the equivalent of 27 soccer fields every minute.",
    "LED light bulbs use up to 90% less energy than incandescent bulbs.",
    "Turning off your faucet while brushing your teeth can save up to 8 gallons of water per day.",
    "A single tree can absorb as much as 48 pounds of CO2 per year.",
    "Over 100 species go extinct every day, mainly due to human activities.",
    "More than half of the world’s wetlands have been destroyed since 1900.",
    "Electric cars produce about half as much CO2 as gasoline-powered cars over their lifetime.",
    "If the world's population lived like the average American, we would need five Earths to sustain them.",
    "Composting food waste reduces the amount of waste going to landfill, which in turn reduces methane emissions.",
    "An estimated 100,000 marine animals die each year from plastic entanglement.",
    "Green roofs can reduce city temperatures by absorbing heat and providing shade.",
    "Wind energy is one of the fastest-growing sources of electricity in the world.",
    "One third of all food produced is lost or wasted, contributing to greenhouse gas emissions.",
    "Switching to a vegetarian diet can reduce your carbon footprint by about 1.5 tons per year.",
    "The Amazon rainforest produces 20% of the world's oxygen supply.",
    "Noise pollution can lead to stress, hearing loss, and increased blood pressure.",
    "Using a reusable water bottle can save an average of 170 plastic bottles per year.",
    "A car's emissions are reduced by 20% when its tires are properly inflated.",
    "E-waste represents 2% of America’s trash in landfills, but it equals 70% of overall toxic waste.",
    "Deforestation contributes to soil erosion and climate change.",
    "Solar energy is the most abundant energy source on Earth.",
    "The fashion industry is responsible for 10% of global carbon emissions.",
    "75% of Earth’s ice-free land has been altered by humans.",
    "More than 3 million people die from illnesses caused by unsafe water every year.",
    "Fossil fuel combustion for electricity and heat is the largest single source of global CO2 emissions.",
    "Planting more trees can significantly reduce air pollution.",
    "Paper products make up the largest percentage of municipal solid waste.",
    "The ocean produces over half of the world’s oxygen and absorbs 50 times more CO2 than the atmosphere.",
    "Mangroves store four times more carbon than most other tropical forests.",
    "Using a cloth bag can save over 700 plastic bags in a person's lifetime.",
    "Globally, 90% of seabirds have plastic in their stomachs.",
    "Green spaces in cities improve mental health and reduce air pollution.",
    "Over 80% of wastewater globally is released back into the environment without treatment.",
    "A quarter of all mammal species face extinction in the next three decades.",
    "Plastic straws can take up to 200 years to decompose.",
    "Every minute, one garbage truck of plastic is dumped into the ocean.",
    "Food production is responsible for up to 30% of global greenhouse gas emissions.",
    "Global warming has caused the average surface temperature of the Earth to rise by about 1.1°C since the late 19th century.",
    "Switching to public transport reduces carbon emissions and congestion.",
    "Microplastics have been found in 93% of bottled water samples.",
    "Coal-fired power plants are the largest contributors to mercury pollution.",
    "Natural disasters are becoming more frequent and intense due to climate change.",
    "Some types of plastic can take up to 1,000 years to decompose.",
    "Seagrasses can capture carbon up to 35 times faster than tropical rainforests.",
    "Nearly 700 species of marine animals are impacted by ocean plastic.",
    "Recycling aluminum saves 90% of the energy required to make new aluminum.",
    "Oceans absorb about 30% of the CO2 released into the atmosphere.",
    "LED street lighting can reduce CO2 emissions significantly compared to conventional lighting.",
    "Reducing meat consumption can decrease greenhouse gas emissions and conserve water.",
    "Industrial agriculture is responsible for 75% of global deforestation.",
    "Most plastic pollution in the ocean originates from rivers.",
    "Methane is over 25 times more potent as a greenhouse gas than CO2.",
    "Each year, humans produce enough plastic to circle the Earth four times.",
    "Oil spills have a catastrophic impact on marine ecosystems.",
    "Eating local reduces the carbon footprint of food transportation.",
    "Coral reefs protect coastlines from storms and erosion.",
    "Around 90% of the world's fish stocks are fully exploited or overfished.",
    "Plant-based diets require less water and land than diets based on animal products.",
    "Using energy-efficient appliances reduces your carbon footprint.",
    "Decomposing organic waste in landfills releases methane, a potent greenhouse gas.",
    "Bamboo grows quickly and is a sustainable alternative to wood.",
    "The hole in the ozone layer is slowly healing thanks to global efforts.",
    "Hybrid cars combine a gasoline engine with electric power, reducing emissions.",
    "Pollution affects more than 200 million people worldwide.",
    "Switching to green energy sources reduces fossil fuel reliance.",
    "More than a million plastic bags are used every minute worldwide.",
    "Rainforests are home to half of the Earth's species.",
    "Renewable energy jobs have been increasing rapidly over the past decade.",
    "Bees and other pollinators are essential for biodiversity.",
    "Reusing materials conserves resources and reduces waste.",
    "Ocean acidification is caused by excess CO2 and harms marine life.",
    "Global warming could lead to a loss of two-thirds of the polar bear population by 2050.",
    "The Arctic is warming twice as fast as the rest of the world.",
    "Disposable diapers take around 500 years to decompose in landfills.",
    "Walking or cycling instead of driving can reduce air pollution.",
    "Switching to LED lighting can cut energy use by up to 75%.",
    "Approximately 11% of greenhouse gas emissions come from deforestation.",
    "Thermal power plants require large amounts of water for cooling.",
    "Around 30% of all bird species face extinction due to habitat loss.",
    "Switching to solar power can significantly reduce energy costs.",
    "Cattle produce methane, a potent greenhouse gas.",
    "Clean water is a finite resource under threat.",
    "Electric cars produce zero emissions.",
    "Using recycled glass reduces air pollution by 20%.",
    "Saving energy reduces greenhouse gas emissions.",
    "The loss of sea ice threatens polar bear survival.",
    "Wind turbines generate electricity without emissions.",
    "Paper waste makes up about 25% of landfill waste.",
    "Sustainable agriculture conserves water and soil quality.",
    "Recycling electronics prevents toxic waste."
]

# Placeholder to retrieve facts
def get_random_fact():
    import random
    return random.choice(environmental_facts)
