import re
from datetime import datetime

from fastapi import Depends, HTTPException
from sqlalchemy import func, or_, case
from sqlalchemy.orm import Session

from fastapi_erp.database import get_db, set_fields_from_dict
from fastapi_erp.model.base.ip import UtiIp
from fastapi_erp.model.base.people import People
from fastapi_erp.model.base.dependency import Dependency
from fastapi_erp.model.base.dependency_type import DependencyType


class IpService:

    @staticmethod
    def instance(db: Session = Depends(get_db)) -> "IpService":
        return IpService(db)

    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def _empty(value):
        if value is None:
            return None

        if isinstance(value, str):
            value = value.strip()
            return value if value else None

        return value

    @staticmethod
    def _like(value, regex=False):
        value = str(value).upper()

        if regex:
            value = re.sub(r"\s+", "%", value)
            value = value.replace("-", "%")
            value = value.replace(":", "%")
            value = value.replace(".", "%")
        else:
            value = value.replace(" ", "%")

        return f"%{value}%"

    async def get(self, id: int):
        return (
            self.db.query(UtiIp)
            .filter(UtiIp.id == id)
            .first()
        )

    async def find(self, ip_id: int):
        item = await self.get(ip_id)

        if item is not None:
            # Equivalente aproximado a setExt(new HashMap<>())
            # si tu modelo realmente tiene este atributo.
            if hasattr(item, "ext"):
                item.ext = {}

        return item

    async def clear(self, id: int):
        entity = await self.find(id)

        if entity is not None:
            entity.creation = None
            entity.updated = None
            entity.name = None
            entity.position = None
            entity.device_model = None
            entity.patrimonial_code = None
            entity.device_serie = None
            entity.mac_id = None
            entity.description = None

        return entity
    
    def load(
        self,
        first: int = 0,
        page_size: int = 100,
        sort_field: str | None = None,
        filters: dict | None = None,
    ):
        #filters = filters or {}

        # ---------------------------------------------------------
        # FILTROS
        # ---------------------------------------------------------

        general_filter = self._empty(filters.get("filter"))
        user = self._empty(filters.get("user"))

        # category es especial en Java:
        # "" significa buscar category vacío/null.
        category = filters.get("category")

        code = self._empty(filters.get("code"))
        name = self._empty(filters.get("name"))
        mac_id = self._empty(filters.get("macId"))
        position = self._empty(filters.get("position"))
        device = self._empty(filters.get("device"))
        siaf = self._empty(filters.get("siaf"))
        user_siaf = self._empty(filters.get("userSiaf"))
        patrimonial_code = self._empty(
            filters.get("patrimonialCode")
        )
        description = self._empty(filters.get("description"))
        dependency = self._empty(filters.get("dependency"))

        # Java lo obtiene, aunque en este método no termina
        # participando en el WHERE.
        empty = self._empty(filters.get("empty"))

        # ---------------------------------------------------------
        # QUERY BASE
        #
        # Java:
        #
        # SELECT o, s.fullName
        # FROM UtiIp o
        # LEFT JOIN People s ON s.id = o.peopleId
        # LEFT JOIN Dependency d ON d.id = o.dependencyId
        # LEFT JOIN d.type t
        # WHERE o.canceled = 0
        # ---------------------------------------------------------

        query = (
            self.db.query(
                UtiIp,
                People.full_name.label("full_name"),
            )
            .outerjoin(
                People,
                People.id == UtiIp.people_id,
            )
            .outerjoin(
                Dependency,
                Dependency.id == UtiIp.dependency_id,
            )
            .outerjoin(
                DependencyType,
                DependencyType.id == Dependency.type_id,
            )
            .filter(UtiIp.canceled == 0)
        )

        # ---------------------------------------------------------
        # CATEGORY
        # ---------------------------------------------------------

        if category is not None:
            category = str(category).strip()

            if category == "":
                query = query.filter(
                    or_(
                        func.trim(UtiIp.category) == "",
                        UtiIp.category.is_(None),
                    )
                )
            else:
                query = query.filter(
                    func.upper(UtiIp.category).like(
                        category.upper().replace(" ", "%")
                    )
                )

        # ---------------------------------------------------------
        # FILTRO GENERAL
        # ---------------------------------------------------------

        if general_filter is not None:
            value = self._like(
                general_filter,
                regex=True,
            )

            query = query.filter(
                or_(
                    func.upper(UtiIp.category).like(value),
                    func.upper(UtiIp.code).like(value),
                    func.upper(UtiIp.name).like(value),
                    func.upper(UtiIp.siaf).like(value),
                    func.upper(UtiIp.mac_id).like(value),
                    func.upper(UtiIp.workgroup).like(value),
                    func.upper(UtiIp.patrimonial_code).like(value),
                    func.upper(UtiIp.user_siaf).like(value),
                    func.upper(UtiIp.position).like(value),
                    func.upper(UtiIp.antivirus).like(value),
                    func.upper(UtiIp.restriction).like(value),
                    func.upper(UtiIp.description).like(value),
                    func.upper(UtiIp.device).like(value),

                    func.upper(DependencyType.name).like(value),
                    func.upper(Dependency.name).like(value),

                    # El Java original también hacía esto.
                    func.upper(UtiIp.stabilizer).like(value),

                    func.upper(UtiIp.stabilizer_code).like(value),
                    func.upper(UtiIp.stabilizer_description).like(value),
                    func.upper(UtiIp.printer_code).like(value),
                    func.upper(UtiIp.printer_description).like(value),
                    func.upper(UtiIp.printer_serie).like(value),
                    func.upper(UtiIp.printer_model).like(value),
                    func.upper(UtiIp.device_serie).like(value),
                    func.upper(UtiIp.device_model).like(value),
                )
            )

        # ---------------------------------------------------------
        # FILTROS ESPECÍFICOS
        # ---------------------------------------------------------

        if code is not None:
            query = query.filter(
                func.upper(UtiIp.code).like(
                    self._like(code)
                )
            )

        if name is not None:
            query = query.filter(
                func.upper(UtiIp.name).like(
                    self._like(name)
                )
            )

        if siaf is not None:
            query = query.filter(
                func.upper(UtiIp.siaf).like(
                    self._like(siaf)
                )
            )

        if mac_id is not None:
            query = query.filter(
                func.upper(UtiIp.mac_id).like(
                    self._like(
                        mac_id,
                        regex=True,
                    )
                )
            )

        if patrimonial_code is not None:
            query = query.filter(
                func.upper(UtiIp.patrimonial_code).like(
                    self._like(patrimonial_code)
                )
            )

        if user_siaf is not None:
            query = query.filter(
                func.upper(UtiIp.user_siaf).like(
                    self._like(user_siaf)
                )
            )

        if position is not None:
            query = query.filter(
                func.upper(UtiIp.position).like(
                    self._like(position)
                )
            )

        if description is not None:
            query = query.filter(
                func.upper(UtiIp.description).like(
                    self._like(description)
                )
            )

        if device is not None:
            query = query.filter(
                func.upper(UtiIp.device).like(
                    self._like(device)
                )
            )

        # ---------------------------------------------------------
        # DEPENDENCY
        #
        # Java:
        #
        # UPPER(CONCAT(t.name, d.name)) LIKE :dependency
        # ---------------------------------------------------------

        if dependency is not None:
            value = self._like(dependency)

            query = query.filter(
                func.upper(
                    func.concat(
                        func.coalesce(
                            DependencyType.name,
                            "",
                        ),
                        func.coalesce(
                            Dependency.name,
                            "",
                        ),
                    )
                ).like(value)
            )

        # ---------------------------------------------------------
        # TOTAL
        #
        # Equivalente a:
        #
        # SELECT COUNT(o) + mismo WHERE
        #
        # Tiene que calcularse ANTES de offset/limit.
        # ---------------------------------------------------------

        if page_size > 0:
            filters["size"] = query.count()

        # ---------------------------------------------------------
        # ORDER BY
        #
        # Java default:
        #
        # o.n3, n4, o.code DESC
        # ---------------------------------------------------------

        sorter = self._empty(
            filters.get("SORTER")
        )

        if sorter:
            parts = str(sorter).split("-", 1)

            field = parts[0]

            direction = (
                parts[1].upper()
                if len(parts) > 1
                else "ASC"
            )

            descending = direction == "DESC"

            if field == "updated":
                query = query.order_by(
                    UtiIp.updated.desc()
                    if descending
                    else UtiIp.updated.asc()
                )

            elif field == "code":
                query = query.order_by(
                    UtiIp.n3.desc()
                    if descending
                    else UtiIp.n3.asc(),

                    UtiIp.n4.desc()
                    if descending
                    else UtiIp.n4.asc(),

                    UtiIp.code.desc()
                    if descending
                    else UtiIp.code.asc(),
                )

            else:
                query = query.order_by(
                    UtiIp.n3.asc(),
                    UtiIp.n4.asc(),
                    UtiIp.code.desc(),
                )

        else:
            query = query.order_by(
                UtiIp.n3.asc(),
                UtiIp.n4.asc(),
                UtiIp.code.desc(),
            )

        # ---------------------------------------------------------
        # PAGINACIÓN
        # ---------------------------------------------------------

        if page_size > 0:
            query = (
                query
                .offset(first)
                .limit(page_size)
            )

        # ---------------------------------------------------------
        # RESULTADO
        #
        # SQLAlchemy devuelve:
        #
        # Row(UtiIp, full_name)
        #
        # Java hacía:
        #
        # AbstractFacade.getColumn(
        #     query.getResultList(),
        #     RowAdapter
        # )
        #
        # y terminaba devolviendo List<UtiIp>.
        # ---------------------------------------------------------

        rows = query.all()

        result: list[UtiIp] = []

        for item, full_name in rows:
            item.ext = {
                "fullName": full_name,
            }

            result.append(item)

        return result
    
    async def edit(self, entity: UtiIp, user=None):
        parts = entity.code.split(".")

        if len(parts) != 4:
            raise HTTPException(
                status_code=400,
                detail=f"El ip={entity.code} no es una direccion valida.",
            )

        try:
            octets = [int(value) for value in parts]
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"El ip={entity.code} no es una direccion valida.",
            )

        # El Java original solamente parseaba los números.
        # Aprovechamos para validar realmente IPv4.
        if any(value < 0 or value > 255 for value in octets):
            raise HTTPException(
                status_code=400,
                detail=f"El ip={entity.code} no es una direccion valida.",
            )

        entity.code = ".".join(str(value) for value in octets)

        entity.n3 = octets[2]
        entity.n4 = octets[3]

        if not entity.canceled:
            query = (
                self.db.query(UtiIp)
                .filter(
                    UtiIp.canceled == 0,
                    UtiIp.code == entity.code,
                )
            )

            print(entity)
            if entity.id is not None:
                query = query.filter(
                    UtiIp.id != entity.id
                )

            if query.first():
                raise HTTPException(
                    status_code=409,
                    detail=f"El ip={entity.code} ya existe.",
                )

        # -----------------------------------------------------
        # Usuario
        # -----------------------------------------------------

        if (
            user is not None
            and getattr(entity, "user", None) is None
        ):
            entity.user = user.id_dir

        # -----------------------------------------------------
        # Fechas / persistencia
        # -----------------------------------------------------

        now = datetime.now()

        if entity.creation is None:
            entity.creation = now

        if entity.id is None:
            self.db.add(entity)
            self.db.flush()
        else:
            entity.updated = now
            entity = self.db.merge(entity)

        return entity

    async def update(
        self,
        ip_id: int,
        new_item: dict,
        user=None,
    ):
        entity = await self.get(ip_id)

        if entity is None:
            raise HTTPException(
                status_code=404,
                detail="IP no encontrada",
            )

        set_fields_from_dict(entity, new_item)

        return await self.edit(entity, user=user)

    def get_category_list(self):
        rows = (
            self.db.query(UtiIp.category)
            .distinct()
            .order_by(UtiIp.category)
            .all()
        )

        return [row[0] for row in rows]

    # ---------------------------------------------------------
    # DISABLE
    # ---------------------------------------------------------

    def disable(self, ids: list[int]):
        if not ids:
            return 0

        result = (
            self.db.query(UtiIp)
            .filter(UtiIp.id.in_(ids))
            .update(
                {
                    UtiIp.active: case(
                        (UtiIp.active == 1, 0),
                        else_=1,
                    )
                },
                synchronize_session=False,
            )
        )

        return result
