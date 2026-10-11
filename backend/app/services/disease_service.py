import re
from typing import Dict, List, Optional
from app.schemas.disease import DiseaseBase

# Curated reference database of crop diseases based on standard agricultural taxonomy
DISEASE_DATABASE: Dict[str, DiseaseBase] = {
    "pepper-bacterial-spot": DiseaseBase(
        id="pepper-bacterial-spot",
        crop="Pepper",
        disease="Bacterial Spot",
        scientific_name="Xanthomonas spp. (bacterial spot species complex)",
        is_healthy=False,
        severity="Moderate",
        symptoms=[
            "Small brown to black, roughly circular leaf spots, often first seen on lower leaves",
            "Spots may enlarge and merge, causing yellowing and leaf drop; pepper leaf spots often lack the yellow halo seen on tomato",
            "Raised, corky brown spots may develop on fruit, commonly near the stem end",
        ],
        causes=[
            "Infection by bacterial spot Xanthomonas species; different strains may affect pepper, tomato, or both",
            "Warm, humid weather and leaf wetness favor infection; bacteria can arrive on seed or transplants and spread in splashing water or on hands and tools",
        ],
        prevention=[
            "Start with reputable, disease-free seed and inspect transplants before planting",
            "Use drip irrigation, avoid working among wet plants, and allow good airflow",
            "Rotate away from pepper and tomato, control volunteer plants, and clean tools and supports",
            "Remove or bury infected crop residue after harvest",
        ],
        management=[
            "Remove symptomatic plants or leaves where practical and avoid moving through wet crops",
            "Disinfect pruning tools between plants and remove crop debris at season end",
            "Ask local extension about registered products; use only products labeled for the crop and follow label directions",
        ],
    ),
    "pepper-healthy": DiseaseBase(
        id="pepper-healthy",
        crop="Pepper",
        disease="Healthy",
        scientific_name="Capsicum annuum",
        is_healthy=True,
        severity="None",
        symptoms=[
            "Leaves are generally uniform green and retain their shape, without distinct lesions, unusual mottling, or progressive yellowing",
            "Stems and growing tips show normal growth without unexplained dieback",
        ],
        causes=["Normal plant growth under suitable light, water, nutrition, and growing conditions"],
        prevention=[
            "Maintain even soil moisture and provide appropriate light and balanced nutrition",
            "Inspect leaves regularly and use clean tools and healthy transplants",
        ],
        management=["No disease treatment is indicated for a healthy plant; continue routine care and monitoring"],
    ),
    "tomato-bacterial-spot": DiseaseBase(
        id="tomato-bacterial-spot",
        crop="Tomato",
        disease="Bacterial Spot",
        scientific_name="Xanthomonas spp. (bacterial spot species complex)",
        is_healthy=False,
        severity="Moderate",
        symptoms=[
            "Small brown, roughly circular leaf spots that may have yellow halos; centers can dry and fall out, leaving small holes",
            "Spots may also occur on stems and fruit; fruit lesions can be raised, brown, and scabby",
            "Severe leaf infection can cause yellowing, defoliation, and reduced fruit quality",
        ],
        causes=[
            "Infection by bacterial spot Xanthomonas species, including X. vesicatoria, X. euvesicatoria, X. gardneri, and X. perforans",
            "Warm, humid conditions and frequent leaf wetness favor infection; bacteria may arrive on seed or transplants and spread by splashing water, hands, and tools",
        ],
        prevention=[
            "Use reputable seed and inspect transplants for spots or discoloration",
            "Avoid overhead irrigation, water at the plant base, and allow foliage to dry quickly",
            "Rotate away from tomato, pepper, and related solanaceous crops; remove volunteer plants and crop residue",
            "Disinfect tools and avoid pruning or handling plants while foliage is wet",
        ],
        management=[
            "Remove symptomatic leaves or plants where practical and avoid spreading bacteria between plants",
            "Clean tools and remove or bury crop residue after harvest",
            "Pesticide options may be limited; consult local extension and use only products labeled for tomatoes, following label directions",
        ],
    ),
    "tomato-early-blight": DiseaseBase(
        id="tomato-early-blight",
        crop="Tomato",
        disease="Early Blight",
        scientific_name="Alternaria solani",
        is_healthy=False,
        severity="Moderate",
        symptoms=[
            "Dark brown to black spots with concentric rings ('target board' pattern) on older leaves",
            "Yellowing (chlorosis) of tissue surrounding the leaf lesions",
            "Premature defoliation starting from the lower canopy moving upward",
            "Dark, sunken stem lesions near the soil line (collar rot)"
        ],
        causes=[
            "Fungal pathogen surviving in plant debris or soil",
            "Warm temperatures (24°C to 29°C) combined with high humidity or frequent rainfall",
            "Overhead watering that keeps foliage wet for prolonged periods"
        ],
        prevention=[
            "Practice 2-3 year crop rotation with non-solanaceous crops",
            "Use drip irrigation or soaker hoses to avoid wetting foliage",
            "Apply organic mulch around plants to prevent soil splashing onto lower leaves",
            "Space plants adequately to facilitate rapid canopy drying and air circulation"
        ],
        management=[
            "Prune and safely dispose of infected lower leaves immediately upon detection",
            "Apply protective copper-based organic fungicides or Mancozeb/Chlorothalonil at early disease signs",
            "Ensure balanced fertilization; avoid excess nitrogen which produces overly dense foliage"
        ]
    ),
    "tomato-late-blight": DiseaseBase(
        id="tomato-late-blight",
        crop="Tomato",
        disease="Late Blight",
        scientific_name="Phytophthora infestans",
        is_healthy=False,
        severity="Critical",
        symptoms=[
            "Large, irregular water-soaked spots on leaves turning dark brown to purplish-black",
            "Delicate white cottony fungal growth on the undersides of leaves during damp conditions",
            "Dark brown blotches on stems and green fruit",
            "Rapid collapse and rotting of entire foliage in cool, wet weather"
        ],
        causes=[
            "Aggressive oomycete water-mold pathogen capable of rapid wind dispersal",
            "Cool, cloudy, and wet weather conditions (15°C to 20°C with 90%+ relative humidity)",
            "Contaminated volunteer plants or infected seed potatoes nearby"
        ],
        prevention=[
            "Plant certified disease-resistant hybrid tomato cultivars",
            "Scout plants frequently during extended cool, humid weather spells",
            "Eliminate all volunteer potato and tomato plants from preceding seasons",
            "Never compost infected plant residue; bag and remove from the field"
        ],
        management=[
            "Apply systemic preventative fungicides (e.g., Metalaxyl, Dimethomorph, or Chlorothalonil)",
            "In commercial fields, harvest marketable fruits promptly if blight is confirmed",
            "Remove and destroy severely blighted plants to curb community spore spread"
        ]
    ),
    "tomato-leaf-mold": DiseaseBase(
        id="tomato-leaf-mold",
        crop="Tomato",
        disease="Leaf Mold",
        scientific_name="Passalora fulva",
        is_healthy=False,
        severity="Moderate",
        symptoms=[
            "Pale greenish-yellow spots, often without distinct margins, on the upper sides of older leaves",
            "Olive-green to brown velvety mold on the lower leaf surface beneath the yellow spots",
            "Affected leaves may turn brown, wither, and die; severe infections can cause substantial defoliation",
            "In severe cases, blossoms may blacken and fall, and fruit may develop dark, leathery lesions near the stem end",
        ],
        causes=[
            "Infection by the fungus Passalora fulva (also known as Fulvia fulva), favored by prolonged high humidity and limited air movement",
            "The pathogen can persist in infected crop debris and may spread on seed, air currents, splashing water, tools, and workers",
        ],
        prevention=[
            "Improve airflow by spacing, staking, and pruning plants, and ventilate greenhouses or high tunnels",
            "Use drip irrigation and avoid wetting foliage; keep humidity around plants as low as practical",
            "Clean reusable stakes, ties, tools, and growing structures, and remove infected crop residue after harvest",
            "Consider locally suitable resistant varieties, while monitoring for disease because resistance can vary by pathogen strain",
        ],
        management=[
            "Remove and dispose of infected leaves and crop debris; avoid handling plants while foliage is wet",
            "Increase ventilation and reduce humidity to limit further infection and spore production",
            "If fungicides are considered, consult local extension guidance and use only products labeled for tomatoes and the production setting, following all label directions",
        ],
    ),
    "tomato-septoria-leaf-spot": DiseaseBase(
        id="tomato-septoria-leaf-spot",
        crop="Tomato",
        disease="Septoria Leaf Spot",
        scientific_name="Septoria lycopersici",
        is_healthy=False,
        severity="Moderate",
        symptoms=[
            "Numerous small, circular leaf spots, usually beginning on lower leaves after fruit set",
            "Spots develop pale gray or tan centers, dark margins, and sometimes a narrow yellow halo; tiny black fungal structures may be visible in the centers",
            "Severely affected leaves yellow, wither, and drop, often progressing upward from the base",
        ],
        causes=[
            "Infection by the fungus Septoria lycopersici, which can persist in infected plant debris and spread in wind-driven or splashing rain",
            "Warm, humid weather and prolonged leaf wetness favor disease development",
        ],
        prevention=[
            "Rotate tomatoes with non-host crops and remove infected crop debris and nearby host weeds",
            "Mulch to reduce soil splash, space and stake plants for airflow, and water at the base rather than over the foliage",
            "Inspect transplants and remove lower leaves that touch the soil once plants are established",
        ],
        management=[
            "Remove infected leaves and crop debris; avoid working among wet plants",
            "Where disease is recurrent or severe, ask local extension about labeled protective fungicides and follow the product label",
        ],
    ),
    "tomato-spider-mites": DiseaseBase(
        id="tomato-spider-mites",
        crop="Tomato",
        disease="Spider Mites",
        scientific_name="Tetranychus urticae (two-spotted spider mite)",
        is_healthy=False,
        severity="Moderate",
        symptoms=[
            "Fine pale stippling or tiny yellow spots on leaves, often first noticeable on the undersides",
            "Heavier feeding can bronze or bleach leaves, cause leaf drop, and produce fine webbing",
            "Mites may be difficult to see without a hand lens; symptoms can resemble drought stress",
        ],
        causes=[
            "Feeding by two-spotted spider mites, which pierce leaf cells and remove their contents",
            "Hot, dry conditions and plant stress can favor rapid mite population growth",
        ],
        prevention=[
            "Scout leaf undersides regularly, especially during hot, dry weather",
            "Keep plants adequately watered without overwatering and conserve predatory mites and other beneficial organisms",
            "Avoid unnecessary broad-spectrum insecticides that can harm natural enemies",
        ],
        management=[
            "Confirm mites on leaf undersides with a hand lens or by shaking foliage over white paper",
            "A directed water spray may dislodge mites; repeat scouting to check whether populations persist",
            "If a miticide, insecticidal soap, or horticultural oil is considered, use only a product labeled for tomatoes and mites, following label directions",
        ],
    ),
    "tomato-target-spot": DiseaseBase(
        id="tomato-target-spot",
        crop="Tomato",
        disease="Target Spot",
        scientific_name="Corynespora cassiicola",
        is_healthy=False,
        severity="Moderate",
        symptoms=[
            "Small dark-brown leaf lesions that enlarge and develop lighter tan to gray centers with darker concentric rings",
            "Lesions may merge, blighting leaves and causing premature defoliation",
            "Dark lesions can form on petioles and stems; fruit may develop sunken, expanding spots",
        ],
        causes=[
            "Infection by the fungus Corynespora cassiicola, which produces spores that spread by wind and rain",
            "Warm conditions, high humidity, dense canopies, and prolonged leaf wetness favor infection",
        ],
        prevention=[
            "Start with healthy transplants and improve canopy airflow through appropriate spacing and staking",
            "Avoid prolonged leaf wetness and overhead irrigation where possible",
            "Rotate with non-solanaceous crops and remove weeds, volunteer tomatoes, and crop debris that may harbor inoculum",
        ],
        management=[
            "Scout regularly because target spot can resemble other tomato leaf spots; seek diagnostic confirmation if uncertain",
            "Remove infected debris and reduce canopy humidity and leaf wetness",
            "For fungicide decisions, consult local extension guidance and follow only products labeled for tomatoes and target spot",
        ],
    ),
    "tomato-yellow-leaf-curl-virus": DiseaseBase(
        id="tomato-yellow-leaf-curl-virus",
        crop="Tomato",
        disease="Yellow Leaf Curl Virus",
        scientific_name="Tomato yellow leaf curl virus (TYLCV)",
        is_healthy=False,
        severity="High",
        symptoms=[
            "Young leaves may show yellowing along margins or between veins and curl upward or downward",
            "Plants can become stunted and bushy, with shortened internodes and smaller leaves",
            "Flower drop and reduced fruit set are common, especially when young plants are infected",
        ],
        causes=[
            "Infection by tomato yellow leaf curl virus, primarily transmitted by whiteflies",
            "Infected transplants and host weeds or other plants can introduce or maintain the virus",
        ],
        prevention=[
            "Use healthy transplants and resistant varieties suited to the region when available",
            "Monitor and manage whiteflies using locally recommended integrated pest management practices",
            "Control volunteer tomatoes and relevant weeds that can serve as virus or whitefly reservoirs",
        ],
        management=[
            "There is no treatment that cures a virus-infected plant; confirm diagnosis because nutrient, herbicide, and other problems can look similar",
            "Remove and dispose of confirmed infected plants to reduce sources of infection; do not compost them",
            "Clean hands and tools and follow local extension guidance for whitefly and virus management",
        ],
    ),
    "tomato-mosaic-virus": DiseaseBase(
        id="tomato-mosaic-virus",
        crop="Tomato",
        disease="Mosaic Virus",
        scientific_name="Tomato mosaic virus (ToMV)",
        is_healthy=False,
        severity="Moderate",
        symptoms=[
            "Leaves may show mottled light and dark green areas and may become curled, malformed, or smaller",
            "Plants infected early can be stunted; fruit may be reduced in size, ripen unevenly, or show discoloration",
            "Symptoms vary by cultivar and can resemble other viruses or non-infectious disorders",
        ],
        causes=[
            "Infection by tomato mosaic virus, which can persist in infected plant debris or seed and spread through contaminated hands, tools, and plant handling",
            "Some weeds and other solanaceous plants may act as virus reservoirs",
        ],
        prevention=[
            "Use clean seed and healthy transplants; select varieties with ToMV resistance where appropriate",
            "Wash hands and disinfect tools and equipment regularly, especially before handling healthy plants",
            "Remove crop debris and avoid handling tobacco products around tomato plants",
        ],
        management=[
            "There is no chemical cure for virus-infected plants; seek diagnostic confirmation because virus symptoms overlap",
            "Remove and dispose of confirmed infected plants rather than composting them",
            "Disinfect tools and hands and follow local extension guidance to reduce further spread",
        ],
    ),
    "tomato-healthy": DiseaseBase(
        id="tomato-healthy",
        crop="Tomato",
        disease="Healthy",
        scientific_name="Solanum lycopersicum",
        is_healthy=True,
        severity="None",
        symptoms=[
            "Lush, uniform green leaf coloration across the canopy",
            "Absence of necrotic spots, lesions, or chlorotic margins",
            "Vigorous stem growth and active flower/fruit set"
        ],
        causes=[
            "Adequate sunlight, balanced soil nutrients, and proper hydration"
        ],
        prevention=[
            "Maintain consistent soil moisture without waterlogging",
            "Provide balanced N-P-K fertilization according to crop development stage",
            "Perform weekly visual inspections to catch early pest or pathogen presence"
        ],
        management=[
            "No chemical or therapeutic intervention needed",
            "Continue standard agronomic and cultural maintenance"
        ]
    ),
    "potato-early-blight": DiseaseBase(
        id="potato-early-blight",
        crop="Potato",
        disease="Early Blight",
        scientific_name="Alternaria solani",
        is_healthy=False,
        severity="Moderate",
        symptoms=[
            "Small, dark brown, angular spots with visible concentric rings on mature leaves",
            "Leaf margins curling and dying as lesions coalesce",
            "Reduced tuber size and yield due to photosynthetic surface loss"
        ],
        causes=[
            "Alternaria fungal spores carried by wind and rain splash",
            "Stressed plants suffering from nutrient deficiency or drought"
        ],
        prevention=[
            "Plant high-vigor, certified seed tubers",
            "Maintain optimal crop nutrition, especially nitrogen and potassium",
            "Rotate crops with non-host species like cereals or legumes"
        ],
        management=[
            "Apply preventative broad-spectrum fungicides like Azoxystrobin or Mancozeb",
            "Irrigate during morning hours so foliage dries quickly under the sun"
        ]
    ),
    "potato-late-blight": DiseaseBase(
        id="potato-late-blight",
        crop="Potato",
        disease="Late Blight",
        scientific_name="Phytophthora infestans",
        is_healthy=False,
        severity="Critical",
        symptoms=[
            "Pale green or dark water-soaked lesions that rapidly expand across foliage",
            "White mildew growth on the leaf underside under high moisture",
            "Tuber rot featuring brown, dry, granular decay penetrating beneath the skin"
        ],
        causes=[
            "Water mold pathogen spread through air currents and infected seed tubers",
            "High humidity and moderate temperatures"
        ],
        prevention=[
            "Hill up soil well over developing tubers to shield them from spores washed from leaves",
            "Destroy all cull piles and volunteer potato sprouts before planting season"
        ],
        management=[
            "Immediately apply curative systemic fungicides upon first localized symptoms",
            "Kill vines 2 weeks prior to harvest if foliage is infected to prevent tuber infection during digging"
        ]
    ),
    "potato-healthy": DiseaseBase(
        id="potato-healthy",
        crop="Potato",
        disease="Healthy",
        scientific_name="Solanum tuberosum",
        is_healthy=True,
        severity="None",
        symptoms=[
            "Stout, upright foliage with rich green coloration and crisp margins",
            "No spotting, mold, or leaf curl"
        ],
        causes=[
            "Optimal agronomic care and disease-free certified tubers"
        ],
        prevention=[
            "Continue clean cultivation and scout weekly"
        ],
        management=[
            "Maintain regular watering and hilling practices"
        ]
    ),
    "corn-common-rust": DiseaseBase(
        id="corn-common-rust",
        crop="Corn (Maize)",
        disease="Common Rust",
        scientific_name="Puccinia sorghi",
        is_healthy=False,
        severity="Moderate",
        symptoms=[
            "Small, cinnamon-brown to golden powdery pustules scattered on upper and lower leaf surfaces",
            "Pustules rupture epidermal tissue, releasing rusty fungal spores",
            "Severe infection leads to leaf chlorosis, necrosis, and diminished ear filling"
        ],
        causes=[
            "Fungal urediniospores blown northward by wind currents from southern corn regions",
            "Cool temperatures (16°C to 24°C) coupled with persistent dews or humidity"
        ],
        prevention=[
            "Select resistant or tolerant hybrid maize varieties (carrying Rp resistance genes)",
            "Plant early in the season to reduce exposure to peak airborne spore flights"
        ],
        management=[
            "Foliar fungicide application (strobilurins or triazoles) if pustules emerge prior to silking on sensitive hybrids"
        ]
    ),
    "apple-apple-scab": DiseaseBase(
        id="apple-apple-scab",
        crop="Apple",
        disease="Apple Scab",
        scientific_name="Venturia inaequalis",
        is_healthy=False,
        severity="Moderate",
        symptoms=[
            "Olive-green to velvety dark brown lesions on the upper leaf surface",
            "Distorted, puckered leaves that drop prematurely in mid-summer",
            "Scabby, cracked lesions on apple fruit skin, impairing marketability"
        ],
        causes=[
            "Ascomycete fungus overwintering on fallen leaf litter on the orchard floor",
            "Spring rains causing primary ascospore discharge onto emerging green tissue"
        ],
        prevention=[
            "Mow, rake, or compost fallen autumn leaves to disrupt overwintering fungal structures",
            "Prune apple canopies annually to allow sunlight penetration and rapid air drying"
        ],
        management=[
            "Apply preventative copper or sulfur fungicides at green-tip and tight-cluster stages",
            "Use myclobutanil or captan during active ascospore discharge periods"
        ]
    )
}


class DiseaseService:
    """Service providing query and retrieval capabilities for the crop disease catalog."""

    @staticmethod
    def get_all_diseases(crop: Optional[str] = None) -> List[DiseaseBase]:
        """Returns all cataloged diseases, optionally filtered by crop name."""
        diseases = list(DISEASE_DATABASE.values())
        if crop:
            crop_clean = crop.strip().lower()
            diseases = [d for d in diseases if d.crop.lower() == crop_clean]
        return diseases

    @staticmethod
    def get_disease_by_id(disease_id: str) -> Optional[DiseaseBase]:
        """Retrieves a specific disease record by its unique slug ID."""
        return DISEASE_DATABASE.get(disease_id.strip().lower())

    @staticmethod
    def get_info_for_prediction(crop: str, disease: str) -> Optional[DiseaseBase]:
        """
        Match normalized crop and disease names to one unambiguous catalog entry.

        Underscores, hyphens, repeated spaces, capitalization, and a repeated crop
        prefix in the disease name are normalized. The crop is always part of the
        match so similarly named conditions from different crops cannot collide.
        """
        def normalize(value: str) -> str:
            # Split common CamelCase boundaries before case folding, then treat
            # dataset separators as equivalent to spaces.
            value = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", value.strip())
            return " ".join(value.replace("_", " ").replace("-", " ").casefold().split())

        normalized_crop = normalize(crop)
        normalized_disease = normalize(disease)
        crop_prefix = f"{normalized_crop} "
        while normalized_disease.startswith(crop_prefix):
            normalized_disease = normalized_disease[len(crop_prefix):]
        # PlantVillage labels include the pepper cultivar token and the full
        # two-spotted mite wording; the API presents their canonical names.
        if normalized_crop == "pepper" and normalized_disease.startswith("bell "):
            normalized_disease = normalized_disease[len("bell "):]
        if normalized_crop == "tomato" and normalized_disease == "spider mites two spotted spider mite":
            normalized_disease = "spider mites"

        matches = [
            entry for entry in DISEASE_DATABASE.values()
            if normalize(entry.crop) == normalized_crop
            and normalize(entry.disease) == normalized_disease
        ]
        return matches[0] if len(matches) == 1 else None
