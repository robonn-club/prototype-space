# Datasets

Data for training, testing and benchmarking, removing the need to record a full dataset before
work can begin.

Licence terms should be read before any dataset is built upon. Non-commercial terms are common in
robotics, and a dataset suitable for publication is not always suitable for a commercial product.
Several major datasets state no licence at all on their download pages. A tag below appears only
where the licence was confirmed; its absence means the terms must be checked directly. See the
Licences section of [certification_resources.md](certification_resources.md).

---

## Agriculture and plants

*Robonn's own domain, and the area where Bonn publishes more than anywhere else.*

- **[Sugar Beets 2016](http://www.ipb.uni-bonn.de/data/sugarbeets2016/)** — Three months of four-channel multispectral, RGB-D, lidar, GPS and wheel-encoder recordings from an agricultural robot at Campus Klein Altendorf near Bonn, around 5 TB in total, and unusually for this field the licence permits commercial use. — `CC BY-SA 4.0`
- **[PhenoBench](https://www.phenobench.org/)** — Uni Bonn's plant phenotyping benchmark: 100-megapixel UAV field imagery with over 5,000 densely annotated plants and 30,000 crop leaves, supporting five segmentation and detection tasks.
- **[BonnBeetClouds3D](https://www.ipb.uni-bonn.de/data/bonnbeetclouds3d/)** — Point clouds of 48 sugar beet varieties across more than 3,000 plants, annotated per plant and per leaf for organ-level phenotyping.
- **[PhenoRoam](https://phenoroam.phenorob.de/geonetwork/srv/eng/catalog.search)** — PhenoRob's own data repository and the catalogue PhenoBench is published in, searchable across the cluster's agricultural and geospatial datasets.
- **[IPB dataset index](https://www.ipb.uni-bonn.de/data/)** — The full dataset list from Uni Bonn's photogrammetry and robotics lab, and the first place to check before looking further afield.
- **[PhenoRob](https://www.phenorob.de/)** — The DFG Cluster of Excellence for crop-production robotics based in Bonn, and the group behind much of the agricultural data above.
- **[EuroCrops](https://github.com/maja601/EuroCrops)** — Harmonised crop-type and parcel-geometry data self-declared by farmers across 17 EU countries, mapped onto a single hierarchical crop taxonomy. — `CC BY-SA 4.0`
- **[EuroCropsML](https://github.com/dida-do/EuroCropsML)** — The analysis-ready derivative of EuroCrops, with roughly 707,000 labelled Sentinel-2 time-series samples across 176 crop classes.
- **[DWD Open Data](https://opendata.dwd.de/)** — The German weather service's open climate and observation records, needed to interpret any outdoor field trial after the fact.

---

## Manipulation and robot learning

*Demonstrations for training manipulation policies.*

- **[Open X-Embodiment](https://robotics-transformer-x.github.io/)** — Over a million real robot trajectories across 22 embodiments, pooled from 60 datasets, with terms that differ per sub-dataset, each requiring separate checking. — `mixed licences`
- **[DROID](https://droid-dataset.github.io/)** — 76,000 demonstration trajectories over 350 hours across 564 scenes and 86 tasks, recorded on Franka Panda arms with two scene stereo cameras, a wrist camera and language annotations on most successful episodes.
- **[RH20T](https://rh20t.github.io/)** — A large manipulation dataset spanning a wide range of contact-rich skills, recorded with multiple camera views and force feedback.
- **[LeRobot datasets](https://huggingface.co/lerobot)** — Datasets published in LeRobotDataset format, loadable directly by the LeRobot stack without conversion.

---

## Driving and perception

*Long-standing benchmarks, used for testing perception before deployment on a robot.*

- **[KITTI](https://www.cvlibs.net/datasets/kitti/)** — The reference autonomous driving benchmark for stereo, optical flow, odometry and detection, restricted to non-commercial use. — `CC BY-NC-SA 3.0`
- **[nuScenes](https://www.nuscenes.org/)** — A full sensor suite including radar across a thousand driving scenes, free for academics and startups with commercial licences sold separately. — `CC BY-NC-SA 4.0`
- **[Waymo Open Dataset](https://waymo.com/open/)** — Large-scale perception, motion and end-to-end driving data, with associated public challenges; the terms of use must be read before any commercial work.
- **[Argoverse 2](https://www.argoverse.org/)** — Autonomous driving data covering sensor recordings, lidar and motion forecasting, with high-definition maps supplied alongside.

---

## SLAM and odometry

*Sequences with ground truth, for measuring whether a mapping or localisation system actually works.*

- **[TUM RGB-D](https://cvg.cit.tum.de/data/datasets/rgbd-dataset)** — Kinect colour and depth sequences at 30 Hz with motion-capture ground truth, and the standard first benchmark for RGB-D SLAM. — `CC BY 4.0`
- **[EuRoC MAV](https://projects.asl.ethz.ch/datasets/doku.php?id=kmavvisualinertialdatasets)** — Stereo and inertial recordings from a micro aerial vehicle with millimetre-accurate ground truth, and the reference benchmark for visual-inertial odometry.
- **[Newer College](https://ori-drs.github.io/newer-college-dataset/)** — Handheld lidar, inertial and vision sequences through indoor and outdoor college grounds, with survey-grade ground truth.
- **[Oxford RobotCar](https://robotcar-dataset.robots.ox.ac.uk/)** — Over a hundred traversals of one Oxford route across a full year, capturing seasonal, weather and construction change for long-term localisation. — `CC BY-NC-SA 4.0`

---

## Space and planetary

*Terrain, navigation and mission data from robots operating where nobody can service them.*

- **[NASA Planetary Data System](https://pds.nasa.gov/)** — NASA's long-term archive of data returned from planetary missions, covering orbital, landed and robotic acquisitions across discipline nodes.
- **[ESA Planetary Science Archive](https://archives.esac.esa.int/psa)** — The European counterpart, holding data returned by ESA's planetary missions.
- **[NASA Open Data Portal](https://data.nasa.gov/)** — The general NASA catalogue, broader than planetary science, and the route to individual mission datasets.
- **[AI4Mars](https://data.nasa.gov/dataset/ai4mars-a-dataset-for-terrain-aware-autonomous-driving-on-mars)** — Terrain segmentation labels over Curiosity, Opportunity and Spirit imagery across four classes of soil, bedrock, sand and large rock, crowdsourced and reviewed by mission rover planners.
- **[DLR Robotics and Mechatronics](https://github.com/DLR-RM)** — Open code and data releases from DLR's robotics institute, including planetary-analogue navigation work.

---

## Indoor and simulation

*Environments for navigation and embodied AI work that begins before any hardware exists.*

- **[Objaverse](https://objaverse.allenai.org/)** — A large library of annotated 3D objects, used to populate manipulation and navigation scenes without modelling every item by hand.
- **[Replica](https://github.com/facebookresearch/Replica-Dataset)** — Eighteen photorealistic indoor reconstructions with dense geometry, HDR textures and semantic and instance segmentation, usable directly in AI Habitat.

---

## Catalogues and search

*Most research data is never packaged as a machine-learning benchmark. These are the routes to it.*

- **[Hugging Face robotics datasets](https://huggingface.co/datasets?task_categories=task_categories:robotics)** — Browsable and filterable, and where most new robot datasets now appear first.
- **[Papers with Code — robotics](https://paperswithcode.com/datasets?mod=robots)** — Datasets indexed against the papers and benchmarks that use them.
- **[re3data](https://www.re3data.org/)** — A registry of more than 3,500 research data repositories, filterable by subject and country, for finding the repository before the dataset.
- **[BonaRes](https://www.bonares.de/)** — The German repository for standardised soil and long-term agricultural field-experiment data, published under FAIR principles.
- **[data.europa.eu](https://data.europa.eu/en)** — The EU open data portal, covering agriculture, environment and geospatial data published by member states.
- **[Google Dataset Search](https://datasetsearch.research.google.com/)** — Indexes datasets across repositories that publish structured metadata, useful when the hosting repository is unknown.
- **[bonndata](https://bonndata.uni-bonn.de/)** — Uni Bonn's own institutional research data repository, filterable by subject including agricultural sciences.
- **[FAIRagro](https://fairagro.net/en/)** — The national infrastructure consortium linking German agrosystems data repositories into one searchable inventory.
- **[OpenAgrar](https://www.openagrar.de/)** — The open-access repository for German agricultural research data, reports and publications.
- **[Copernicus Data Space](https://dataspace.copernicus.eu/)** — Sentinel satellite imagery for Europe, the standard source for field-scale remote sensing.
- **[awesome-robotics-datasets](https://github.com/sunglok/awesome-robotics-datasets)** — A curated index of robotics datasets, covering the ground these sections do not.
