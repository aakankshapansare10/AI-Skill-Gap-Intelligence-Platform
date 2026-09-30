--
-- PostgreSQL database dump
--

\restrict Ro9Zajs5JljaJujRSiivs40PYwEUuGpsvkaSm528uphPvZMahEKgxzUzee5fcnO

-- Dumped from database version 18.6
-- Dumped by pg_dump version 18.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: domain_skill_demand; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.domain_skill_demand (
    domain_id integer NOT NULL,
    skill_id integer NOT NULL,
    rank integer,
    job_count integer,
    total_jobs integer,
    demand_percentage numeric
);


ALTER TABLE public.domain_skill_demand OWNER TO postgres;

--
-- Name: domain_skill_demand_staging; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.domain_skill_demand_staging (
    domain_id bigint,
    skill_id bigint,
    rank integer,
    job_count bigint,
    total_jobs bigint,
    demand_percentage numeric
);


ALTER TABLE public.domain_skill_demand_staging OWNER TO postgres;

--
-- Name: domains; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.domains (
    domain_id integer NOT NULL,
    domain_name text NOT NULL
);


ALTER TABLE public.domains OWNER TO postgres;

--
-- Name: job_domains; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.job_domains (
    job_id bigint NOT NULL,
    domain_id integer NOT NULL
);


ALTER TABLE public.job_domains OWNER TO postgres;

--
-- Name: job_domains_staging; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.job_domains_staging (
    job_id bigint,
    domain_id integer
);


ALTER TABLE public.job_domains_staging OWNER TO postgres;

--
-- Name: job_skills; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.job_skills (
    job_id bigint CONSTRAINT job_skills_job_id_not_null1 NOT NULL,
    skill_id integer CONSTRAINT job_skills_skill_id_not_null1 NOT NULL
);


ALTER TABLE public.job_skills OWNER TO postgres;

--
-- Name: job_skills_nlp_staging; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.job_skills_nlp_staging (
    job_id bigint NOT NULL,
    skill_id integer NOT NULL,
    skill_name text
);


ALTER TABLE public.job_skills_nlp_staging OWNER TO postgres;

--
-- Name: job_skills_nlp_v13; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.job_skills_nlp_v13 (
    job_id bigint NOT NULL,
    skill_id integer NOT NULL,
    skill_name text NOT NULL,
    canonical_skill_name text
);


ALTER TABLE public.job_skills_nlp_v13 OWNER TO postgres;

--
-- Name: job_skills_old; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.job_skills_old (
    job_id bigint CONSTRAINT job_skills_job_id_not_null NOT NULL,
    skill_id integer CONSTRAINT job_skills_skill_id_not_null NOT NULL
);


ALTER TABLE public.job_skills_old OWNER TO postgres;

--
-- Name: job_skills_old_backup; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.job_skills_old_backup (
    job_id bigint,
    skill_id integer
);


ALTER TABLE public.job_skills_old_backup OWNER TO postgres;

--
-- Name: job_skills_staging; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.job_skills_staging (
    job_id bigint,
    skill_id integer
);


ALTER TABLE public.job_skills_staging OWNER TO postgres;

--
-- Name: jobs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.jobs (
    job_id bigint NOT NULL,
    title text,
    company_name text,
    location text,
    experience text,
    salary text,
    job_description text,
    minimum_salary numeric,
    maximum_salary numeric,
    minimum_experience numeric,
    maximum_experience numeric
);


ALTER TABLE public.jobs OWNER TO postgres;

--
-- Name: skills; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.skills (
    skill_id integer NOT NULL,
    skill_name text NOT NULL
);


ALTER TABLE public.skills OWNER TO postgres;

--
-- Name: ml_job_skills; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.ml_job_skills AS
 SELECT j.job_id,
    j.title AS job_title,
    s.skill_id,
    s.skill_name
   FROM ((public.job_skills js
     JOIN public.jobs j ON ((js.job_id = j.job_id)))
     JOIN public.skills s ON ((js.skill_id = s.skill_id)));


ALTER VIEW public.ml_job_skills OWNER TO postgres;

--
-- Name: skill_demand; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.skill_demand (
    skill_id integer NOT NULL,
    rank integer,
    job_count integer,
    demand_percentage numeric
);


ALTER TABLE public.skill_demand OWNER TO postgres;

--
-- Name: skill_demand_staging; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.skill_demand_staging (
    skill_id bigint,
    total_jobs bigint,
    total_job_postings bigint,
    demand_percentage numeric
);


ALTER TABLE public.skill_demand_staging OWNER TO postgres;

--
-- Name: domain_skill_demand domain_skill_demand_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.domain_skill_demand
    ADD CONSTRAINT domain_skill_demand_pkey PRIMARY KEY (domain_id, skill_id);


--
-- Name: domains domains_domain_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.domains
    ADD CONSTRAINT domains_domain_name_key UNIQUE (domain_name);


--
-- Name: domains domains_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.domains
    ADD CONSTRAINT domains_pkey PRIMARY KEY (domain_id);


--
-- Name: job_domains job_domains_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_domains
    ADD CONSTRAINT job_domains_pkey PRIMARY KEY (job_id);


--
-- Name: job_skills_old job_skills_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_skills_old
    ADD CONSTRAINT job_skills_pkey PRIMARY KEY (job_id, skill_id);


--
-- Name: job_skills job_skills_pkey1; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_skills
    ADD CONSTRAINT job_skills_pkey1 PRIMARY KEY (job_id, skill_id);


--
-- Name: jobs jobs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jobs
    ADD CONSTRAINT jobs_pkey PRIMARY KEY (job_id);


--
-- Name: skill_demand skill_demand_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill_demand
    ADD CONSTRAINT skill_demand_pkey PRIMARY KEY (skill_id);


--
-- Name: skills skills_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skills
    ADD CONSTRAINT skills_pkey PRIMARY KEY (skill_id);


--
-- Name: skills skills_skill_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skills
    ADD CONSTRAINT skills_skill_name_key UNIQUE (skill_name);


--
-- Name: domain_skill_demand domain_skill_demand_domain_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.domain_skill_demand
    ADD CONSTRAINT domain_skill_demand_domain_id_fkey FOREIGN KEY (domain_id) REFERENCES public.domains(domain_id) ON DELETE CASCADE;


--
-- Name: domain_skill_demand domain_skill_demand_skill_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.domain_skill_demand
    ADD CONSTRAINT domain_skill_demand_skill_id_fkey FOREIGN KEY (skill_id) REFERENCES public.skills(skill_id) ON DELETE CASCADE;


--
-- Name: job_domains job_domains_domain_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_domains
    ADD CONSTRAINT job_domains_domain_id_fkey FOREIGN KEY (domain_id) REFERENCES public.domains(domain_id) ON DELETE CASCADE;


--
-- Name: job_domains job_domains_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_domains
    ADD CONSTRAINT job_domains_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(job_id) ON DELETE CASCADE;


--
-- Name: job_skills_old job_skills_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_skills_old
    ADD CONSTRAINT job_skills_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(job_id) ON DELETE CASCADE;


--
-- Name: job_skills job_skills_job_id_fkey1; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_skills
    ADD CONSTRAINT job_skills_job_id_fkey1 FOREIGN KEY (job_id) REFERENCES public.jobs(job_id) ON DELETE CASCADE;


--
-- Name: job_skills_old job_skills_skill_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_skills_old
    ADD CONSTRAINT job_skills_skill_id_fkey FOREIGN KEY (skill_id) REFERENCES public.skills(skill_id) ON DELETE CASCADE;


--
-- Name: job_skills job_skills_skill_id_fkey1; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_skills
    ADD CONSTRAINT job_skills_skill_id_fkey1 FOREIGN KEY (skill_id) REFERENCES public.skills(skill_id) ON DELETE CASCADE;


--
-- Name: skill_demand skill_demand_skill_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill_demand
    ADD CONSTRAINT skill_demand_skill_id_fkey FOREIGN KEY (skill_id) REFERENCES public.skills(skill_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict Ro9Zajs5JljaJujRSiivs40PYwEUuGpsvkaSm528uphPvZMahEKgxzUzee5fcnO

