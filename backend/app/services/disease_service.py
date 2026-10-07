from typing import Dict, List, Optional
from app.schemas.disease import DiseaseBase

# Curated reference database of crop diseases based on standard agricultural taxonomy
DISEASE_DATABASE: Dict[str, DiseaseBase] = {
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
        Matches a prediction classification (e.g. crop="Tomato", disease="Early Blight")
        to the corresponding clinical entry in the disease catalog.
        """
        slug = f"{crop.strip().lower()}-{disease.strip().lower().replace(' ', '-')}"
        if slug in DISEASE_DATABASE:
            return DISEASE_DATABASE[slug]

        # Fallback search if slug pattern varies
        for entry in DISEASE_DATABASE.values():
            if (
                entry.crop.lower() == crop.strip().lower()
                and entry.disease.lower() == disease.strip().lower()
            ):
                return entry

        return None
